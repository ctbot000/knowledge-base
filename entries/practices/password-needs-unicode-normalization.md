---
title: A password hashed without Unicode normalization does not match the same letters sent in another normalization form
tags: [unicode, auth, security]
added: 2026-10-03
sources:
  - https://www.rfc-editor.org/rfc/rfc8265#section-4.2
  - https://unicode.org/reports/tr15/
---

## Fact

Many letters have more than one Unicode encoding: "é" is U+00E9 or "e"
followed by U+0301, and a Hangul syllable is one code point in NFC or two
or three conjoining jamo in NFD. A hash compares bytes, so a password set
in one form and typed or pasted in the other hashes differently, and the
right password is rejected.

## Why it matters

Users with non-ASCII passwords are locked out depending on the keyboard,
operating system or source they paste from, and nothing in the error says
why. ASCII-only tests never show it.

## How to apply

- Normalize to NFC before hashing, both when the password is set and when
  it is checked: `password.normalize('NFC')` in JavaScript,
  `unicodedata.normalize('NFC', s)` in Python. RFC 8265 (the PRECIS
  OpaqueString profile) prescribes NFC for passwords.
- Check length limits after normalizing, counting code points rather than
  UTF-16 units.
- Do not apply NFKC or case folding to passwords: they change the secret
  itself, and RFC 8265 keeps passwords case-sensitive.
- Test with an accented or Hangul password set in NFC and entered in NFD.
