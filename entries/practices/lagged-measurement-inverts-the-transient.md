---
title: A response driven only by a lagged measurement moves the wrong way at the start of a step
tags: [control, simulation, modelling]
added: 2026-09-20
---

## Fact

When a system's response is computed from a measurement of its own input, and
that measurement lags the input, the response lags it too — by the sum of both
time constants. If the quantity being regulated depends on the *ratio* of the
two, it moves in the wrong direction until the slower signal catches up.

A ventilation model driven from oxygen uptake showed it clearly: uptake rises
with a ~30 s time constant, ventilation was given a 12 s lag on top of it, so at
the onset of hard work CO2 production outran ventilation and arterial CO2 rose
by 27 mmHg while saturation fell to 88% — the opposite of what starting to
exercise does.

## Why it matters

Both lags are individually correct and defensible, and the steady state is
right, so nothing looks wrong except the transient. The symptom lands in the
regulated variable, several steps downstream, so it gets attributed to that
part: to the gas-exchange equations, to a threshold, to a limit somewhere.

## How to apply

- Feed the response forward from the *demand*, not from the measured
  consequence of it: `drive = max(measured, demanded)`. Real regulators do the
  same thing — the neural component of exercise hyperpnoea exists precisely
  because the chemical one is too slow.
- Lag the feed-forward term too, but less than the process it anticipates, or
  the response steps to its final value while the load is still at rest and
  overshoots as hard in the other direction.
- Close the loop on the regulated variable itself, so any residual error is
  corrected rather than integrated.
- Test the transient, not only the steady state: step the input and assert the
  regulated variable stays in range throughout.
