---
title: No official free API gives stock prices across several countries' exchanges
tags: [market-data, apis, licensing]
added: 2026-11-06
sources:
  - https://twelvedata.com/pricing
  - https://github.com/ranaroussi/yfinance/issues/2480
---

## Fact

As of late 2026, free keyed plans cover US stocks and little else (Twelve Data's is listed
as non-display, for testing and side projects), and the well-known keyless sources decide
for themselves whom they answer: Yahoo's chart endpoints return 429 to many non-browser
clients, and Stooq's downloads sit behind a JavaScript proof-of-work page.

## Why it matters

A design that assumes "just call Yahoo" works in a notebook one day and fails in
production the next. Showing prices to the public is also a separate question from
fetching them: free plans and unofficial feeds rarely grant the right to redistribute.

## How to apply

- Probe from the machine that will really fetch, with an honest client name. A wall or a
  429 is an answer: use another source rather than dressing up as a browser.
- Read `robots.txt` per host. The JSON hosts behind a finance site can differ from its
  pages, and a host that disallows everything rules out that host's endpoints.
- Fetch on one server and hand clients the result, so upstream sees one small client
  whatever the audience, and a browser's CORS rules stop mattering.
- Keep the source behind one module, keep the last good data, and tell whoever owns the
  product when a feed is unofficial or unlicensed.
- Exchange rates are the easy part: the ECB's daily rates are free and keyless through
  Frankfurter.
