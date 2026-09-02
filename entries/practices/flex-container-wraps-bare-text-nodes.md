---
title: A bare text node in a flex container becomes its own flex item
tags: [css, flexbox, layout, frontend]
added: 2026-09-02
sources:
  - https://www.w3.org/TR/css-flexbox-1/#flex-items
---

## Fact

Flex layout does not lay out inline content; it lays out flex items. Any
non-empty run of text directly inside a flex container is wrapped in an
*anonymous flex item* of its own, as a sibling of the element boxes around it.

So this markup, in a `flex-direction: column` container, renders on two lines
rather than one:

```html
<label>Focus <span class="unit">min</span></label>
```

`Focus ` becomes one anonymous item and the `<span>` another, and the column
direction puts each on its own row. The `<span>` being `display: inline` changes
nothing — that property describes how a box participates in inline layout, and
inside a flex container it is blockified and never gets the chance.

## Why it matters

The markup looks like ordinary inline content, so the split reads as a wrapping
or width bug and invites `white-space: nowrap` or a width bump, neither of which
helps. In a `row` container it is easier to miss entirely: the text and the span
sit side by side as intended, but they are now two items, so `gap`,
`justify-content`, `flex: 1` and `:first-child` all count one more item than the
markup suggests.

## How to apply

- Wrap the text in an element so the pair is one item:
  `<span class="lbl">Focus <span class="unit">min</span></span>`.
- Treat "every child of a flex or grid container is an item, including bare
  text" as the rule when counting items for `gap` or `nth-child`.
- The same anonymous-item rule applies to grid containers.
- Whitespace-only text between elements is not wrapped, so ordinary formatting
  newlines in the markup do not create phantom items.
