---
title: GitHub Pages does not render the math that GitHub.com renders in the same file
tags: [github-pages, jekyll, mathjax]
added: 2026-09-06
sources:
  - https://kramdown.gettalong.org/converter/html.html
  - https://docs.mathjax.org/en/latest/options/input/tex.html
---

## Fact

GitHub.com typesets `$…$` and `$$…$$` in Markdown files. GitHub Pages does not:
Jekyll's kramdown treats only `$$…$$` as math and rewrites it to `\[…\]`, and
leaves inline `$…$` in the output as literal text. So the same file reads
correctly in the repository and shows raw TeX on the published site.

MathJax 3 already recognises `\[…\]` as display math, so the whole gap is closed
by registering `$` as an inline delimiter — no kramdown configuration is needed.
Under CommonMark (`markdown: CommonMarkGhPages`) nothing is rewritten at all and
`$$…$$` arrives verbatim, so configure both delimiter pairs and the layout stops
depending on which processor is in use.

## Why it matters

The failure is silent and asymmetric: display equations start working as soon as
MathJax is loaded, which reads as "math works", while every inline expression
stays as dollar signs.

## How to apply

Load MathJax in the layout and add one delimiter:

```html
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']]
    },
    options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }
  };
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

Turn smart punctuation off. CommonMark's `SMART` option (and kramdown's
`smart_quotes`) rewrites straight quotes everywhere, math included, so
`$f'(x)$` reaches MathJax as `$f’(x)$` and the prime is silently lost.

Subscripts survive: neither processor applies emphasis to intra-word `_`, so
`$a_1$` arrives intact. MathJax cannot break math across lines, inline math
included, so give the content column `overflow-x: auto` or one long expression
widens the whole page.
