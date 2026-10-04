---
title: Puppeteer drives a multi-finger gesture with one TouchHandle per finger
tags: [testing, automation, puppeteer, touch, cdp]
added: 2026-10-05
sources:
  - https://pptr.dev/api/puppeteer.touchhandle
---

## Fact

`page.touchscreen.touchStart(x, y)` returns a `TouchHandle`; its `move()` and
`end()` move or lift that finger alone while the others stay down. That covers
pinches, a third finger joining, and lifting one finger of two first. The
events arrive as trusted `pointerType: 'touch'` pointer events without any
`hasTouch` emulation.

Underneath, each call sends CDP `Input.dispatchTouchEvent` with only its own
point, `touchEnd` included, although the protocol's description says touchEnd
"must not contain any touch points". In raw CDP, a `touchMove` that leaves a
finger out does not lift it; a `touchEnd` lifts exactly the points it lists,
and an empty one lifts every finger.

## Why it matters

Going by the protocol text, a raw-CDP test sends `touchMove` without the
finger it means to lift ("one event per changed point, compared to the
previous event"); the finger stays down, and the test silently keeps pinching.

## How to apply

```js
const one = await page.touchscreen.touchStart(100, 200);
const two = await page.touchscreen.touchStart(160, 200);
for (let i = 1; i <= 20; i++) {
  await one.move(100 - i * 3, 200);
  await two.move(160 + i * 3, 200);
}
await two.end(); // the first finger is still down
await one.move(130, 200);
await one.end();
```

Each `move()` is its own event, so one step of a pinch arrives as two
pointermoves. Coordinates are rounded to whole pixels. Where the page lets the
browser pan (no `touch-action: none` up to a scroll container), a finger that
moves becomes a pan and its lift arrives as `pointercancel`, as on a device.

Related: [[setpointercapture-throws-for-inactive-pointer-id]].
