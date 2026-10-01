---
title: scrollWidth and clientWidth round away the sub-pixel overflow that already puts an ellipsis on text
tags: [dom, testing, typography]
added: 2026-10-02
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollWidth
---

## Fact

`scrollWidth` and `clientWidth` are integers. A box 0.05 px narrower than its
text reports the same value for both (143 and 143 in Chrome 154) while
`text-overflow: ellipsis` is already cutting the text, so the usual
`el.scrollWidth > el.clientWidth` truncation check says it fits.

## Why it matters

Layout tests that guard a label against truncation pass while the label on
screen ends in "…". Fractional widths are everywhere: flex shrinking,
percentages and font metrics all produce them.

## How to apply

Compare fractional widths, the text's own extent from a Range against its box:

```js
const text = document.createRange();
text.selectNodeContents(el);
const fits = text.getBoundingClientRect().width <= el.getBoundingClientRect().width;
```

Subtract the box's horizontal padding and borders when it has any.
