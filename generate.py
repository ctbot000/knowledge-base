#!/usr/bin/env python3
"""Build the browsable site for this knowledge base into _site/.

The Markdown under entries/ is the source of truth and the only thing a human
writes. This reads every entry, takes its one-line summary from its topic index,
and writes a static site: one page per entry, plus an index that filters by
topic, tag and free text.

Nothing it writes is committed — a workflow runs it on every push and hands
_site/ straight to GitHub Pages. Run it locally the same way:

    python3 generate.py && python3 -m http.server -d _site
"""

import html
import os
import pathlib
import posixpath
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "_site"
KST = timezone(timedelta(hours=9))
REPO = os.environ.get("GITHUB_REPOSITORY") or "ctbot000/knowledge-base"
BLOB = f"https://github.com/{REPO}/blob/main"

TAGLINE = "Durable, general engineering knowledge, written to be read by an AI coding agent and by a human."

# From README.md's layout section. A topic with no blurb still renders.
BLURBS = {
    "languages": "Language-level behavior, semantics, idioms.",
    "tools": "Build tools, version control, CLIs, editors.",
    "practices": "Testing, review, design, process.",
    "systems": "Databases, networking, performance, distributed behavior.",
    "agents": "Working with LLM coding agents: prompts, skills, harnesses.",
}


# --------------------------------------------------------------------------- #
# Markdown
#
# A deliberately small subset: what CONVENTIONS.md asks an entry to contain —
# headings, paragraphs, lists, fenced code, links, emphasis, the occasional
# table or quote. Anything outside it is reported rather than silently dropped.
# --------------------------------------------------------------------------- #

IN_ACTIONS = bool(os.environ.get("GITHUB_ACTIONS"))

# Root documents that become a page of their own rather than an entry page.
ROOT_DOCS = {"conventions.md": "conventions.html", "index.md": "index.html",
             "readme.md": "index.html"}


def warn(message, file=None):
    """A warning that shows up as an annotation when this runs in Actions."""
    if IN_ACTIONS:
        where = f" file={file}" if file else ""
        print(f"::warning{where}::{message}", file=sys.stderr)
    else:
        print(f"warning: {message}" + (f" ({file})" if file else ""), file=sys.stderr)


def md_href(url):
    """Rewrite a link between Markdown files into the link between their pages.

    Entries link to each other by filename — `[rescue](sibling-entry.md)` — which
    is right in the repository and a 404 on the site.
    """
    if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith(("#", "/", "//")):
        return url
    path, sep, frag = url.partition("#")
    if not path.lower().endswith(".md"):
        return url
    name = path.rsplit("/", 1)[-1].lower()
    if "/" not in path and name in ROOT_DOCS:
        path = ROOT_DOCS[name]
    else:
        path = path[:-3] + ".html"
    return path + sep + frag


FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w+-]*)\s*$")
BULLET_RE = re.compile(r"^(\s*)([-*+])\s+(.*)$")
ORDERED_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?(?:\s*:?-{2,}:?\s*\|)+\s*:?-{2,}:?\s*\|?\s*$")


def inline(text):
    """Inline Markdown to HTML. Code spans are stashed first so nothing else
    reaches inside them."""
    spans = []

    def stash(m):
        spans.append(html.escape(m.group(1)))
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{md_href(m.group(2))}">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_(?=\S)([^_\n]+?)(?<=\S)_(?![\w_])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{spans[int(m.group(1))]}</code>", text)


def _closes(line, fence):
    m = re.match(r"^\s*(`{3,}|~{3,})\s*$", line)
    return bool(m) and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)


def _collect_item(lines, i, indent):
    """Lines belonging to the list item that starts at lines[i], de-indented."""
    body = [BULLET_RE.match(lines[i]).group(3) if BULLET_RE.match(lines[i])
            else ORDERED_RE.match(lines[i]).group(3)]
    i += 1
    pad = " " * (indent + 2)
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].startswith(pad):
                body.extend([""] * (j - i))
                i = j
                continue
            break
        if line.startswith(pad):
            body.append(line[indent + 2:])
            i += 1
            continue
        if BULLET_RE.match(line) or ORDERED_RE.match(line) or HEADING_RE.match(line) \
                or FENCE_RE.match(line) or HR_RE.match(line) or QUOTE_RE.match(line):
            break
        body.append(line.strip())  # lazy continuation of the item's paragraph
        i += 1
    return body, i


def _item_html(body):
    inner = render(body).strip()
    m = re.fullmatch(r"<p>(.*)</p>", inner, re.S)
    return m.group(1) if m else inner


def render(lines):
    """Block-level Markdown to HTML. `lines` is a list of raw lines."""
    if isinstance(lines, str):
        lines = lines.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        m = FENCE_RE.match(line)
        if m:
            indent, fence, lang = m.group(1), m.group(2), m.group(3)
            i += 1
            code = []
            while i < len(lines) and not _closes(lines[i], fence):
                raw = lines[i]
                code.append(raw[len(indent):] if raw.startswith(indent) else raw.lstrip())
                i += 1
            i += 1
            cls = f' class="lang-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre>")
            continue

        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        if QUOTE_RE.match(line):
            quoted = []
            while i < len(lines) and QUOTE_RE.match(lines[i]):
                quoted.append(QUOTE_RE.match(lines[i]).group(1))
                i += 1
            out.append(f"<blockquote>{render(quoted)}</blockquote>")
            continue

        if "|" in line and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]

            head = cells(line)
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(cells(lines[i]))
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows
            )
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>")
            continue

        m = BULLET_RE.match(line) or ORDERED_RE.match(line)
        if m:
            ordered = bool(ORDERED_RE.match(line))
            indent = len(m.group(1))
            items = []
            while i < len(lines):
                nxt = ORDERED_RE.match(lines[i]) if ordered else BULLET_RE.match(lines[i])
                if not nxt or len(nxt.group(1)) != indent:
                    if not lines[i].strip():
                        j = i
                        while j < len(lines) and not lines[j].strip():
                            j += 1
                        peek = (ORDERED_RE if ordered else BULLET_RE).match(lines[j]) if j < len(lines) else None
                        if peek and len(peek.group(1)) == indent:
                            i = j
                            continue
                    break
                body, i = _collect_item(lines, i, indent)
                items.append(f"<li>{_item_html(body)}</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        para = []
        while i < len(lines) and lines[i].strip():
            if para and (BULLET_RE.match(lines[i]) or ORDERED_RE.match(lines[i])
                         or HEADING_RE.match(lines[i]) or FENCE_RE.match(lines[i])
                         or QUOTE_RE.match(lines[i]) or HR_RE.match(lines[i])):
                break
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")

    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Reading the repository
# --------------------------------------------------------------------------- #

def parse_entry(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: no front matter")
    i = 1
    fm = []
    while i < len(lines) and lines[i].strip() != "---":
        fm.append(lines[i])
        i += 1
    body = lines[i + 1:]

    meta = {"tags": [], "sources": [], "title": path.stem, "added": "", "updated": ""}
    key = None
    for line in fm:
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key == "sources":
            meta["sources"].append(item.group(1).strip())
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*?)\s*(?:#.*)?$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2)
        if key == "tags":
            meta["tags"] = [t.strip() for t in value.strip("[]").split(",") if t.strip()]
        elif key == "sources":
            meta["sources"] = []
        else:
            meta[key] = value

    return meta, body


def first_sentence(body):
    """Fallback summary: the opening sentence of the Fact section."""
    text = []
    seen_fact = False
    for line in body:
        if line.startswith("## "):
            if seen_fact:
                break
            seen_fact = line.strip().lower() == "## fact"
            continue
        if seen_fact and line.strip():
            text.append(line.strip())
        elif text:
            break
    joined = re.sub(r"`([^`]+)`", r"\1", " ".join(text))
    m = re.match(r"(.+?[.!?])(\s|$)", joined)
    return m.group(1) if m else joined


def read_index():
    """Summaries, topic order and entry order, taken from the indexes an agent
    actually reads: INDEX.md links the topic indexes, and each of those lists its
    entries relative to itself. The curated order is the one worth showing."""
    summaries, topics, order = {}, [], []
    toc = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    indexes = list(dict.fromkeys(re.findall(r"\]\((entries/[^/)\s]+/INDEX[^/)\s]*\.md)\)", toc)))
    for index in indexes:
        path = ROOT / index
        if not path.exists():
            warn(f"{index} is linked from INDEX.md but missing on disk", file="INDEX.md")
            continue
        if path.parent.name not in topics:
            topics.append(path.parent.name)
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^-\s+\[.+?\]\(([^)\s]+)\)\s+—\s+(.*?)\s*$", line)
            if not m:
                continue
            rel = posixpath.normpath(posixpath.join(posixpath.dirname(index), m.group(1)))
            if rel in summaries:
                warn(f"{rel} is listed more than once", file=index)
                continue
            summaries[rel] = re.sub(r"\s*(?:`[\w.+-]+`,?\s*)+$", "", m.group(2))
            order.append(rel)
    for path in sorted(ROOT.glob("entries/*/INDEX*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel not in indexes:
            warn(f"{rel} is not linked from INDEX.md", file=rel)
    return summaries, topics, order


def load_entries():
    summaries, topic_order, entry_order = read_index()
    rank = {path: i for i, path in enumerate(entry_order)}

    entries = []
    for path in sorted(ROOT.glob("entries/*/*.md")):
        if path.name.startswith("INDEX"):
            continue  # a topic index, not an entry
        rel = path.relative_to(ROOT).as_posix()
        meta, body = parse_entry(path)
        entries.append({
            "topic": path.parent.name,
            "slug": path.stem,
            "src": rel,
            "url": rel[:-3] + ".html",
            "title": meta["title"],
            "tags": meta["tags"],
            "added": meta["added"],
            "updated": meta["updated"],
            "sources": meta["sources"],
            "summary": summaries.get(rel) or first_sentence(body),
            "body": body,
        })

    orphans = [e["src"] for e in entries if e["src"] not in rank]
    dangling = [p for p in entry_order if not (ROOT / p).exists()]
    for label, paths in (("is not listed in any topic index", orphans),
                         ("is listed in a topic index but missing on disk", dangling)):
        for path in paths:
            warn(f"{path} {label}", file=path)

    # Curated order first, then anything the index has not picked up yet.
    entries.sort(key=lambda e: (rank.get(e["src"], len(rank)), e["src"]))

    topics = [t for t in topic_order if any(e["topic"] == t for e in entries)]
    topics += sorted({e["topic"] for e in entries} - set(topics))
    return entries, topics


# --------------------------------------------------------------------------- #
# The page
# --------------------------------------------------------------------------- #

CSS = """
:root {
  color-scheme: light dark;
  --bg: #f6f7f9;
  --bg-elev: #ffffff;
  --fg: #14171c;
  --fg-muted: #5b6472;
  --fg-faint: #8b93a1;
  --line: #e3e6eb;
  --line-strong: #d0d5dd;
  --accent: #2f6fed;
  --accent-soft: #e8f0ff;
  --code-bg: #f0f2f5;
  --shadow: 0 1px 2px rgba(16,24,40,.06), 0 8px 24px -12px rgba(16,24,40,.18);
  --radius: 14px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0e1116;
    --bg-elev: #161b22;
    --fg: #e6edf3;
    --fg-muted: #9aa5b1;
    --fg-faint: #6e7781;
    --line: #262c36;
    --line-strong: #333b46;
    --accent: #6ea8ff;
    --accent-soft: #16243d;
    --code-bg: #1b222c;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR",
        Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }
code, pre, kbd { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }
.wrap { max-width: 960px; margin: 0 auto; padding: 0 20px 72px; }

header.top { padding: 56px 0 26px; }
h1 { margin: 0 0 8px; font-size: 30px; letter-spacing: -.02em; }
h1 .at { color: var(--fg-faint); font-weight: 400; }
.tagline { margin: 0; color: var(--fg-muted); font-size: 15px; max-width: 62ch; }
.meta { margin: 14px 0 0; color: var(--fg-faint); font-size: 13px; }
.meta a { color: var(--accent); }
.meta .dot { padding: 0 6px; opacity: .6; }

.controls {
  position: sticky; top: 0; z-index: 10;
  margin: 0 -20px 26px; padding: 12px 20px;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: saturate(180%) blur(12px);
  border-bottom: 1px solid var(--line);
}
.search {
  display: block; width: 100%; padding: 10px 13px;
  font: inherit; color: var(--fg);
  background: var(--bg-elev);
  border: 1px solid var(--line-strong); border-radius: 10px;
}
.search:focus { outline: 2px solid var(--accent); outline-offset: 1px; border-color: transparent; }
.search::placeholder { color: var(--fg-faint); }
.pills { display: flex; flex-wrap: wrap; align-items: center; gap: 7px; margin-top: 10px; }
.pill {
  padding: 5px 12px; font: inherit; font-size: 13px; cursor: pointer;
  color: var(--fg-muted); background: var(--bg-elev);
  border: 1px solid var(--line-strong); border-radius: 999px;
}
.pill:hover { color: var(--fg); }
.pill[aria-pressed="true"] {
  color: var(--accent); background: var(--accent-soft);
  border-color: color-mix(in srgb, var(--accent) 45%, transparent);
}
.pill .n { color: var(--fg-faint); margin-left: 5px; font-variant-numeric: tabular-nums; }
.pills .spacer { flex: 1; }
.pills .count { color: var(--fg-faint); font-size: 12.5px; font-variant-numeric: tabular-nums; }

section.topic { margin: 0 0 34px; }
section.topic > h2 {
  display: flex; align-items: baseline; gap: 9px;
  margin: 0 0 3px; font-size: 17px; letter-spacing: -.01em;
}
section.topic > h2 .count {
  font-size: 12px; font-weight: 500; color: var(--fg-faint);
  font-variant-numeric: tabular-nums;
}
section.topic > .blurb { margin: 0 0 12px; color: var(--fg-faint); font-size: 13px; }

ul.rows { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
li.row {
  position: relative;
  padding: 14px 16px 12px;
  background: var(--bg-elev);
  border: 1px solid var(--line); border-radius: var(--radius);
  box-shadow: var(--shadow);
  transition: transform .12s ease, border-color .12s ease;
}
li.row:hover { transform: translateY(-1px); border-color: color-mix(in srgb, var(--accent) 40%, var(--line)); }
li.row h3 { margin: 0 0 5px; font-size: 15.5px; line-height: 1.4; letter-spacing: -.01em; }
li.row h3 a::after { content: ""; position: absolute; inset: 0; }
li.row p { margin: 0; color: var(--fg-muted); font-size: 13.5px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 9px; }
.tag {
  position: relative; z-index: 1;
  padding: 2px 9px; font: inherit; font-size: 11.5px; cursor: pointer;
  color: var(--fg-faint); background: transparent;
  border: 1px solid var(--line-strong); border-radius: 999px;
}
.tag:hover { color: var(--accent); border-color: color-mix(in srgb, var(--accent) 45%, transparent); }

.empty { display: none; padding: 48px 0; color: var(--fg-faint); text-align: center; }
body.no-results .empty { display: block; }
[hidden] { display: none !important; }

article.entry { max-width: 720px; }
.crumbs { padding: 40px 0 0; font-size: 13px; color: var(--fg-faint); }
.crumbs a { color: var(--accent); }
.crumbs .sep { padding: 0 6px; opacity: .6; }
article.entry > h1 { margin: 16px 0 10px; font-size: 27px; line-height: 1.25; }
.entry-meta { margin: 0 0 22px; color: var(--fg-faint); font-size: 12.5px; }
.entry-meta .dot { padding: 0 6px; opacity: .6; }
.prose h2 {
  margin: 34px 0 10px; padding-top: 16px;
  font-size: 15px; letter-spacing: .02em; text-transform: uppercase;
  color: var(--fg-muted); border-top: 1px solid var(--line);
}
.prose h3 { margin: 24px 0 8px; font-size: 16px; }
.prose p, .prose li { color: var(--fg); }
.prose p { margin: 0 0 14px; }
.prose ul, .prose ol { margin: 0 0 14px; padding-left: 22px; }
.prose li { margin: 0 0 7px; }
.prose li > ul, .prose li > ol { margin: 7px 0 0; }
.prose a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
.prose code { padding: 1.5px 5px; font-size: 87%; background: var(--code-bg); border-radius: 5px; }
.prose pre {
  margin: 0 0 16px; padding: 13px 15px; overflow-x: auto;
  background: var(--code-bg); border: 1px solid var(--line); border-radius: 10px;
  font-size: 13px; line-height: 1.5;
}
.prose pre code { padding: 0; background: none; font-size: inherit; }
.prose blockquote {
  margin: 0 0 16px; padding: 2px 0 2px 15px;
  border-left: 3px solid var(--line-strong); color: var(--fg-muted);
}
.prose blockquote p { margin: 0; }
.prose table { width: 100%; margin: 0 0 16px; border-collapse: collapse; font-size: 13.5px; }
.prose th, .prose td { padding: 7px 10px; text-align: left; border: 1px solid var(--line); }
.prose th { background: var(--code-bg); font-weight: 600; }
.prose hr { margin: 24px 0; border: 0; border-top: 1px solid var(--line); }
.sources { margin: 30px 0 0; padding-top: 16px; border-top: 1px solid var(--line); }
.sources h2 { margin: 0 0 8px; font-size: 12px; letter-spacing: .04em; text-transform: uppercase; color: var(--fg-faint); }
.sources ul { margin: 0; padding-left: 18px; }
.sources li { margin: 0 0 5px; font-size: 13px; word-break: break-all; }
.sources a { color: var(--accent); }

nav.prevnext { display: flex; gap: 12px; margin-top: 34px; }
nav.prevnext a {
  flex: 1; padding: 12px 14px;
  background: var(--bg-elev); border: 1px solid var(--line); border-radius: var(--radius);
  font-size: 13px; color: var(--fg-muted);
}
nav.prevnext a:hover { border-color: color-mix(in srgb, var(--accent) 40%, var(--line)); color: var(--fg); }
nav.prevnext .dir { display: block; margin-bottom: 3px; font-size: 11px; color: var(--fg-faint); }
nav.prevnext .next { text-align: right; }

footer.bot {
  margin-top: 44px; padding-top: 20px;
  border-top: 1px solid var(--line);
  color: var(--fg-faint); font-size: 12.5px;
}
footer.bot a { color: var(--accent); }
@media (max-width: 560px) {
  header.top { padding: 34px 0 20px; }
  h1 { font-size: 24px; }
  article.entry > h1 { font-size: 23px; }
  nav.prevnext { flex-direction: column; }
}
"""

JS = """
(function () {
  var search = document.getElementById('search');
  var pills = Array.prototype.slice.call(document.querySelectorAll('.pill'));
  var rows = Array.prototype.slice.call(document.querySelectorAll('li.row'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('section.topic'));
  var count = document.getElementById('count');
  var topic = 'all';

  function apply() {
    var terms = search.value.toLowerCase().split(/\\s+/).filter(Boolean);
    var shown = 0;
    rows.forEach(function (row) {
      var hay = row.getAttribute('data-search');
      var ok = (topic === 'all' || row.getAttribute('data-topic') === topic) &&
               terms.every(function (t) { return hay.indexOf(t) !== -1; });
      row.hidden = !ok;
      if (ok) shown++;
    });
    sections.forEach(function (s) {
      var visible = Array.prototype.slice.call(s.querySelectorAll('li.row'))
        .filter(function (r) { return !r.hidden; }).length;
      s.hidden = visible === 0;
      var n = s.querySelector('h2 .count');
      if (n) n.textContent = visible === s.querySelectorAll('li.row').length
        ? n.getAttribute('data-total') : visible + ' of ' + n.getAttribute('data-total');
    });
    count.textContent = shown + (shown === 1 ? ' entry' : ' entries');
    document.body.classList.toggle('no-results', shown === 0);
  }

  search.addEventListener('input', apply);

  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      topic = pill.getAttribute('data-topic');
      pills.forEach(function (p) { p.setAttribute('aria-pressed', p === pill ? 'true' : 'false'); });
      apply();
    });
  });

  document.addEventListener('click', function (e) {
    var tag = e.target.closest ? e.target.closest('.tag') : null;
    if (!tag) return;
    e.preventDefault();
    search.value = tag.getAttribute('data-tag');
    topic = 'all';
    pills.forEach(function (p) {
      p.setAttribute('aria-pressed', p.getAttribute('data-topic') === 'all' ? 'true' : 'false');
    });
    apply();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== search) {
      e.preventDefault();
      search.focus();
      search.select();
    } else if (e.key === 'Escape' && document.activeElement === search) {
      search.value = '';
      apply();
    }
  });

  var q = new URLSearchParams(window.location.search).get('q');
  if (q) search.value = q;
  apply();
})();
"""


def page(title, body, depth=0, description="", script=""):
    desc = f'<meta name="description" content="{html.escape(description)}">' if description else ""
    js = f"<script>{script}</script>" if script else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{desc}
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='14'>&#128218;</text></svg>">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
{js}
</body>
</html>
"""


def footer(depth=0):
    up = "../" * depth
    return (
        '<footer class="bot">'
        f'Generated from the Markdown in <a href="https://github.com/{REPO}">{REPO}</a>'
        f' &middot; <a href="{up}conventions.html">Conventions</a>'
        "</footer>"
    )


def row_html(e):
    tags = "".join(
        f'<button class="tag" data-tag="{html.escape(t, quote=True)}">{html.escape(t)}</button>'
        for t in e["tags"]
    )
    hay = html.escape(
        " ".join([e["title"], e["summary"], " ".join(e["tags"]), e["topic"]]).lower(), quote=True
    )
    return (
        f'<li class="row" data-topic="{e["topic"]}" data-search="{hay}">'
        f'<h3><a href="{e["url"]}">{html.escape(e["title"])}</a></h3>'
        f'<p>{inline(e["summary"])}</p>'
        f'<div class="tags">{tags}</div>'
        "</li>"
    )


def build_index(entries, topics):
    counts = {t: sum(1 for e in entries if e["topic"] == t) for t in topics}
    pills = [
        f'<button class="pill" data-topic="all" aria-pressed="true">All'
        f'<span class="n">{len(entries)}</span></button>'
    ]
    pills += [
        f'<button class="pill" data-topic="{t}" aria-pressed="false">{html.escape(t)}'
        f'<span class="n">{counts[t]}</span></button>'
        for t in topics
    ]

    sections = []
    for t in topics:
        rows = "".join(row_html(e) for e in entries if e["topic"] == t)
        blurb = BLURBS.get(t, "")
        sections.append(
            f'<section class="topic" id="{t}">'
            f'<h2>{html.escape(t)}<span class="count" data-total="{counts[t]}">{counts[t]}</span></h2>'
            + (f'<p class="blurb">{html.escape(blurb)}</p>' if blurb else "")
            + f'<ul class="rows">{rows}</ul>'
            "</section>"
        )

    built = datetime.now(KST).strftime("%Y-%m-%d")
    body = f"""<header class="top">
<h1>knowledge base</h1>
<p class="tagline">{html.escape(TAGLINE)}</p>
<p class="meta">{len(entries)} entries<span class="dot">&middot;</span>{len(topics)} topics<span class="dot">&middot;</span>built {built} KST<span class="dot">&middot;</span><a href="https://github.com/{REPO}">source</a><span class="dot">&middot;</span><a href="conventions.html">conventions</a></p>
</header>

<div class="controls">
<input id="search" class="search" type="search" placeholder="Search titles, summaries and tags&nbsp;&nbsp;(press /)" autocomplete="off" spellcheck="false">
<div class="pills">{''.join(pills)}<span class="spacer"></span><span id="count" class="count"></span></div>
</div>

{''.join(sections)}
<p class="empty">Nothing matches that.</p>
{footer()}"""

    return page(
        "knowledge base",
        body,
        description=TAGLINE,
        script=JS,
    )


def build_entry(e, prev_e, next_e):
    tags = "".join(
        f'<a class="tag" href="../../index.html?q={html.escape(t, quote=True)}">{html.escape(t)}</a>'
        for t in e["tags"]
    )
    dates = [f'added {html.escape(e["added"])}'] if e["added"] else []
    if e["updated"] and e["updated"] != e["added"]:
        dates.append(f'updated {html.escape(e["updated"])}')
    dates.append(f'<a href="{BLOB}/{e["src"]}">view source</a>')

    sources = ""
    if e["sources"]:
        items = "".join(
            f'<li><a href="{html.escape(s, quote=True)}">{html.escape(s)}</a></li>'
            for s in e["sources"]
        )
        sources = f'<div class="sources"><h2>Sources</h2><ul>{items}</ul></div>'

    nav = []
    if prev_e:
        nav.append(
            f'<a class="prev" href="../../{prev_e["url"]}"><span class="dir">&larr; previous in {e["topic"]}</span>'
            f'{html.escape(prev_e["title"])}</a>'
        )
    if next_e:
        nav.append(
            f'<a class="next" href="../../{next_e["url"]}"><span class="dir">next in {e["topic"]} &rarr;</span>'
            f'{html.escape(next_e["title"])}</a>'
        )
    nav_html = f'<nav class="prevnext">{"".join(nav)}</nav>' if nav else ""

    body = f"""<p class="crumbs"><a href="../../index.html">knowledge base</a><span class="sep">/</span><a href="../../index.html#{e["topic"]}">{html.escape(e["topic"])}</a></p>
<article class="entry">
<h1>{html.escape(e["title"])}</h1>
<p class="entry-meta">{'<span class="dot">&middot;</span>'.join(dates)}</p>
<div class="tags">{tags}</div>
<div class="prose">
{render(e["body"])}
</div>
{sources}
{nav_html}
</article>
{footer(depth=2)}"""

    return page(e["title"], body, depth=2, description=e["summary"])


def build_conventions():
    lines = (ROOT / "CONVENTIONS.md").read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else "Conventions"
    body = f"""<p class="crumbs"><a href="index.html">knowledge base</a><span class="sep">/</span>conventions</p>
<article class="entry">
<h1>{html.escape(title)}</h1>
<p class="entry-meta">What belongs here, what does not, and how an entry is written<span class="dot">&middot;</span><a href="{BLOB}/CONVENTIONS.md">view source</a></p>
<div class="prose">
{render(lines[1:])}
</div>
</article>
{footer()}"""
    return page("Conventions · knowledge base", body, description="What belongs in this knowledge base and how an entry is written.")


def build_404():
    body = f"""<header class="top">
<h1>Not here</h1>
<p class="tagline">That page does not exist. Every entry is listed on the index.</p>
<p class="meta"><a href="/knowledge-base/">Back to the index</a></p>
</header>
{footer()}"""
    return page("Not found · knowledge base", body)


def check_links():
    """Every relative link in the built site has to land on a file that exists."""
    broken = 0
    for page_path in sorted(OUT.rglob("*.html")):
        for href in re.findall(r'href="([^"]+)"', page_path.read_text(encoding="utf-8")):
            if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith(("#", "//", "/")):
                continue
            path = re.split(r"[?#]", href, maxsplit=1)[0]
            if not path:
                continue
            target = (page_path.parent / path).resolve()
            if not target.exists():
                warn(f"broken link to {href}", file=str(page_path.relative_to(OUT)))
                broken += 1
    return broken


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    entries, topics = load_entries()
    if not entries:
        print("error: no entries found", file=sys.stderr)
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)

    write(OUT / "index.html", build_index(entries, topics))
    write(OUT / "conventions.html", build_conventions())
    write(OUT / "404.html", build_404())

    for topic in topics:
        group = [e for e in entries if e["topic"] == topic]
        for i, e in enumerate(group):
            write(OUT / e["url"], build_entry(e, group[i - 1] if i else None,
                                              group[i + 1] if i + 1 < len(group) else None))

    broken = check_links()
    print(f"{len(entries)} entries across {len(topics)} topics -> {OUT.relative_to(ROOT)}/"
          + (f" ({broken} broken link(s))" if broken else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
