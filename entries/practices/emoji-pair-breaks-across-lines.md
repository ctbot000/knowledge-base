---
title: Two adjacent emoji can be split across lines, so an emoji pair in a shrinking box turns into a column
tags: [css, typography, flexbox]
added: 2026-10-01
sources:
  - https://www.unicode.org/reports/tr14/
  - https://www.w3.org/TR/css-text-3/#line-breaking
  - https://www.w3.org/TR/css-flexbox-1/#min-size-auto
---

## Fact

Line breaking treats most emoji like CJK ideographs (class `ID` in Unicode's
line breaking algorithm), so a browser may break between two emoji with no
space between them, and between an emoji and a letter. Sequences stay whole: a
ZWJ family, a skin-tone modifier, an emoji with its presentation selector.
Measured in Chromium in a narrow box: `🌅🌧️` takes 2 lines, `🌅🌧️🌈` 3,
`🇰🇷🇯🇵` 2, while `ab`, `👨‍👩‍👧` and `👍🏽` stay on 1.

## Why it matters

An indicator made of two emoji (sun and rain, a status and a badge) looks like
one unbreakable token. Once its box narrows, typically as a flex item when a
toolbar runs out of room, it stacks vertically, doubles its height, and pushes
the row over whatever sits below it. It only happens on the narrowest screens
and only while the second emoji is showing, so it escapes ordinary testing.

## How to apply

- Put `white-space: nowrap` on any element whose text is a run of emoji meant
  to read as one symbol.
- In a flex row, also give it and its fixed-size siblings `flex: none`. A
  declared `width` does not stop a flex item shrinking: its automatic minimum
  is the smaller of that width and its content, so a 40×40 round button squashes
  to an oval (30.7×40 measured). Let one item, a label with `min-width: 0` and
  `text-overflow: ellipsis`, absorb the squeeze instead.
- Test the crowded state: the narrowest supported width with the longest emoji
  combination showing, and measure heights, not just widths.

Related: [[korean-text-breaks-between-syllables]], [[auto-grid-track-blocks-flex-shrink]].
