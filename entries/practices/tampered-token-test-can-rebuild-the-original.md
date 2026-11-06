---
title: A test that tampers with a token by overwriting its end with a constant sometimes leaves it unchanged
tags: [testing, security, flaky-tests]
added: 2026-11-06
---

## Fact

Replacing the last characters of a signature or token with a fixed string, to get
a "bad" one, gives back the original whenever it already ends that way. For two
base64 characters at the end of a 64-byte signature that is 1 run in 256, not 1 in
4096: the last character carries only two bits of signature, the rest being zero,
so far fewer endings are possible than the alphabet suggests.

## Why it matters

The check under test is right, and the test fails anyway, as "accepted a bad
token": it reads like a security hole, comes back rarely, and passes on a rerun,
so it gets written off as noise and retried for as long as anyone notices.

## How to apply

- Change the value rather than setting it: flip a bit of the decoded bytes, or pick
  a replacement that differs from what is there.
- Assert that the tampered token differs from the original before asserting that
  it is refused, so a slip like this fails with a message that says so.
