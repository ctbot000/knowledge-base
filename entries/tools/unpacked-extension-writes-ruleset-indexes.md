---
title: Chrome writes compiled declarativeNetRequest rulesets into an unpacked extension's own folder
tags: [chrome-extensions, git, packaging]
added: 2026-09-23
---

## Fact

Loading an unpacked Manifest V3 extension that declares static rulesets makes
Chrome create `_metadata/generated_indexed_rulesets/` inside the extension
directory, with one binary index per ruleset (`_ruleset1`, `_ruleset2`, ...),
each about as large as the JSON it was built from. The folder comes back every
time anything loads the directory: a developer, a test runner, a build step that
validates rules in a real browser.

## Why it matters

A bulk `git add`, or zipping the folder for a release or the Chrome Web Store,
picks up megabytes of Chrome's private cache; a package can more than double in
size. Nothing fails, so only reading the staged list or the archive listing
catches it.

## How to apply

- Ignore it relative to the extension folder, e.g. `extension/_metadata/`, not
  just at the repository root.
- Exclude `_metadata` by name in packaging scripts; a dotfile filter misses it.
- Deleting it is always safe; Chrome rebuilds the indexes on the next load.
