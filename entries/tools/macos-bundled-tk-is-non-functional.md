---
title: The Tk that ships with macOS is non-functional, not merely old
tags: [tkinter, macos, gui]
added: 2026-09-23
updated: 2026-09-23
---

## Fact

A system Python on macOS links against Apple's bundled Tk 8.5.9, released in
2010 and deprecated by Apple for years. On a current macOS it does not work at
all, in two ways that look like different bugs:

- **It composites nothing.** A bare `Tk()` with a `Frame(bg="#f2f3f5")`, an
  `Entry`, and a `Canvas(bg="white")` holding a red rectangle renders as one
  flat dark box. `cget("bg")` reads the colours back correctly; they are simply
  never drawn. Native controls still paint, so a window can show its buttons
  and its title while its entire content area stays blank.
- **Its event loop does not pump on demand.** `root.update()` called from a
  script never returns — the process sits in the C call indefinitely, while
  `update_idletasks()` and `mainloop()` both behave normally.

Installing a Python built against Tk 8.6 or newer fixes both at once. Verify
with `root.tk.call("info", "patchlevel")`, not with the Python version.

## Why it matters

Neither symptom names its cause. A blank window reads as a drawing bug in the
application, and sends you looking for a paint path that is in fact working
perfectly. A hung `update()` reads as a deadlock in the code under test, and
sends you adding guards against re-entrant event handlers that were never
involved. Both cost hours before the toolkit is suspected at all, because
"Python has tkinter" is normally where that question stops.

## How to apply

- Check the Tk patchlevel before debugging any drawing or event-loop problem
  on macOS, and have the program itself refuse to pretend:

  ```python
  version = root.tk.call("info", "patchlevel")      # e.g. "8.5.9"
  if tuple(int(p) for p in version.split(".")[:2]) < (8, 6):
      print("Tk %s cannot draw on a current desktop." % version)
  ```

- Install a current Tk rather than a different Python version:
  `brew install python-tk@3.13` (match the Homebrew Python you already have)
  binds it to Tk 9.
- Ship a headless path — a text or vector renderer — so a GUI toolkit that
  cannot draw does not make the whole program useless.
- For any suspected hang, `faulthandler.dump_traceback_later(n, exit=True)`
  names the blocking frame immediately; print statements do not.
