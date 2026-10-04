---
title: A browser test that closes its page only when it passes leaves the page running when it fails, and every later test slows down
tags: [testing, automation, ci, puppeteer, browser]
added: 2026-10-04
sources:
  - https://pptr.dev/api/puppeteer.browsercontext.close
  - https://nodejs.org/api/test.html#aftereachfn-options
---

## Fact

When each test closes its page or browser context as its last statement, a
failed assertion or a timed-out wait skips the close. The page stays open in
the shared browser for the rest of the run. With the launch flags test suites
usually pass to keep background pages awake (`--disable-renderer-backgrounding`,
`--disable-background-timer-throttling`), and software rendering on CI, an
animated page keeps drawing at full speed. It takes CPU from every test that
follows. One leaked page of a 3D app made the same later tests run about 3×
slower.

## Why it matters

One failure cascades. Slower tests cross their own per-test timeouts, each of
those leaks its pages too, and the job hits its overall time limit. The log
then shows a cancelled run with no failure details, because the test runner
prints its summary only at the end. Most of the failures look like slowness,
not like the one real bug.

## How to apply

- Close pages where a failure cannot skip it: in `finally`, or in an `afterEach`
  that closes every browser context except the default one
  (`for (const c of browser.browserContexts()) if (c !== browser.defaultBrowserContext()) await c.close()`).
- To spot it in a CI log, compare each test's duration with the last good run.
  Tests before the first failure take their usual time; every test after it is
  uniformly 2-3× slower.
- To confirm it, force the first test to fail and time the same later tests
  with and without the leaked page, under CI-like slowness
  ([[taskpolicy-slows-a-browser-to-ci-speed]]).
