---
title: Usernames unique only up to case still admit look-alike duplicates; fold width with NFKC and refuse invisible characters
tags: [unicode, auth, security]
added: 2026-10-03
sources:
  - https://www.rfc-editor.org/rfc/rfc8265#section-3.3
  - https://www.unicode.org/reports/tr36/
---

## Fact

Lowercasing makes "Minji" and "MINJI" one username, but full-width
"ＭＩＮＪＩ", a name with a zero-width space or joiner inside, or one with
a right-to-left override are still different strings that render the same
or nearly so. A uniqueness check on `toLowerCase()` alone lets each of
them be registered as a separate account.

## Why it matters

Two accounts that look identical let one user impersonate another, and a
user who types the full-width form on a CJK keyboard cannot log in to the
account they made with half-width letters.

## How to apply

- Compare and index usernames by a key: `name.normalize('NFKC').toLowerCase()`
  (Python: `unicodedata.normalize('NFKC', s).casefold()`), after trimming
  and collapsing spaces; RFC 8265's UsernameCaseMapped profile maps width
  and case the same way. Keep the name as typed (NFC) for display.
- Refuse names containing invisible characters: in JavaScript,
  `/\p{C}/u` catches controls, format characters (zero-width joiners,
  bidirectional overrides), private-use and unassigned code points.
- Rate-limit failed logins per key, not per string as typed, or each
  spelling gets its own allowance.
- Passwords are the opposite case: NFC only, no case or width folding (see
  the entry on password normalization).
