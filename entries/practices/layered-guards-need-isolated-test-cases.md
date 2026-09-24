---
title: A test of layered guards still passes with one guard deleted unless some case trips only that guard
tags: [testing, security, mutation-testing]
added: 2026-09-24
---

## Fact

When a request must pass several independent checks (source address, Host
header, key; path validation plus a sandboxed open), a test case that violates
two of them is rejected by whichever runs first. Delete either guard and the
test still passes, because the other one still rejects the request.

## Why it matters

Defense in depth quietly becomes a single layer: the suite is green, coverage
looks complete, and a refactor that drops one check ships unnoticed. It only
shows up when someone deliberately removes each guard and watches for a
failing test.

## How to apply

- For each guard, write a case that satisfies every other guard and fails only
  that one, such as a remote client that sends a forged `Host: localhost` for
  a loopback check.
- Check the suite by mutation: comment out one guard at a time and confirm a
  test fails. A guard whose removal nothing notices has no test.
- Watch the defaults of test fixtures. Go's `httptest.NewRequest` comes from
  `192.0.2.1:1234` with `Host: example.com`, so a loopback-only handler rejects
  it before the check you meant to exercise; set `RemoteAddr` and `Host` on
  purpose.
