---
title: One ACTIVITY_PAUSED does not mean the app left the foreground
tags: [android, usage-stats, instrumentation]
added: 2026-09-02
---

## Fact

Android's usage event stream reports activities, not apps. `ACTIVITY_PAUSED` for
one activity says nothing about whether the *package* is still in front: another
activity of the same app can still be resumed, and since Android 10 several
activities may be resumed at once in multi-window.

## Why it matters

Anything deriving foreground time from these events — screen-time reporting,
session analytics, dwell measurement — under-counts if it closes the session on
the first `ACTIVITY_PAUSED`. A user who opens a dialog-shaped activity, or splits
the screen, stops accruing time while still visibly using the app. The error is
silent and always in the same direction, so the numbers just look plausibly low.

## How to apply

Key the foreground state on the package and keep the set of resumed activity class
names for it. Close the session when that set empties, when a different package
resumes, or when the screen goes non-interactive:

```
RESUMED(pkg, cls)  -> if pkg != current: close(); current = pkg; resumed = {cls}
                      else: resumed += cls
PAUSED(pkg, cls)   -> if pkg == current: resumed -= cls; if resumed.isEmpty(): close()
SCREEN_OFF         -> close()
```

Also clip sessions to the reporting window at both ends, and query events from
before the window starts, or a session that began the previous evening is lost.
