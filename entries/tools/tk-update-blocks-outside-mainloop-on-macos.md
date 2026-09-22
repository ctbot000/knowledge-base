---
title: On macOS, Tk's update() never returns when called outside mainloop()
tags: [tkinter, testing, macos]
added: 2026-09-23
---

## Fact

`root.update()` on a Tk window blocks forever on macOS when it is called from a
plain script rather than from inside `mainloop()`. It is not a slow call: the
interpreter sits inside the C `update` for as long as you let it, and a
`faulthandler` dump shows the whole stack as one frame in
`tkinter/__init__.py`.

`root.update_idletasks()` returns normally, and `mainloop()` with a callback
scheduled by `after()` runs exactly as expected, geometry and all. Reproducing
it needs nothing but `tkinter.Tk()`, `geometry()` and `update()` — no widgets,
no application code.

## Why it matters

`update()` is the obvious way to drive a GUI from a test: build the window,
pump the event loop once, assert on what got drawn. On macOS that test hangs
with no output and no traceback, which reads as a deadlock in the code under
test rather than in the toolkit call meant to observe it. The usual next move —
adding guards against re-entrant event handlers — changes nothing, because the
handlers were never the problem.

## How to apply

- Drive a headless Tk test from the real event loop: schedule the assertions
  with `after()` and call `mainloop()`, ending with `destroy()`.

  ```python
  window = build_the_window()

  def check():
      assert window.canvas.find_all()
      window.root.destroy()

  window.root.after(500, check)
  window.root.mainloop()
  ```

- Use `update_idletasks()` when all that is needed is for pending geometry to
  be recalculated.
- Wrap any suspected hang in `faulthandler.dump_traceback_later(n, exit=True)`
  before reaching for print statements: it names the blocking frame directly.
