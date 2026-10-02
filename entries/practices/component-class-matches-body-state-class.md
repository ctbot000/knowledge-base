---
title: A component class that shares its name with a state class on <body> styles the whole page
tags: [css, cascade, frontend]
added: 2026-10-02
sources:
  - https://www.w3.org/TR/selectors-4/#class-html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/opacity
---

## Fact

A class selector matches any element that has the class. Scripts often put
state flags on `<body>` or `<html>` (`touch`, `dark`, `mobile`, `playing`).
A component rule written as a bare class with the same name, such as
`.touch { width: 60px; opacity: 0.92; font-size: 1.6rem }` for buttons on
touch screens, then also styles the page itself whenever that state is on.

## Why it matters

The page survives it, so nobody looks there. Fixed and absolutely positioned
layers are placed against the viewport, so a body shrunk to 60x60 px still
lays out normally. An `opacity` below 1 draws everything, a full-screen
canvas included, as one translucent group over the root background, which
reads as a faint wash rather than a fault. A `font-size` reaches every
descendant that does not set its own, so only some text grows (bold labels,
paragraphs in dialogs). It happens only on the devices that set the flag,
where it looks like a design choice.

## How to apply

- Keep the two kinds of name apart: `is-touch` or `data-input="touch"` on the
  root, and `.btn-touch` on components.
- Where the names already collide, qualify the component rule (`.btn.touch`,
  `button.touch`), then check that its own modifiers still outrank it.
- On the devices that set state classes on the root, assert that
  `document.body` is still the size of the viewport, with `opacity: 1`.
