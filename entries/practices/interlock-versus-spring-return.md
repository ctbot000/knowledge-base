---
title: A control that springs back to mid-scale can never satisfy an interlock that tests for the end of its travel
tags: [ui, control, game-design, safety]
added: 2026-09-20
---

## Fact

Safety interlocks are written against a resting position: "the throttle must be
at idle before the motors can start", "the blade guard must be closed", "the
form must be untouched". Separately, a control is often given a spring return
to a *neutral* that is not the end of its travel — a centre detent that means
"hold what you have" rather than "off".

Put the two together and the interlock becomes unsatisfiable. The control
cannot be at the end of its travel when released, because releasing it is
exactly what moves it to the middle, so the gate refuses for a position the
operator cannot see and cannot hold.

## Why it matters

It presents as a mode that can be selected and then never used, with an error
message naming a control the operator believes they are not touching. That
reads as a broken check rather than as two correct rules that contradict each
other, so the fix gets attempted by loosening the interlock — which is the one
part that should not move.

It survives testing because each half is usually verified in the regime where
it makes sense: the interlock in the mode where the control rests at the end,
the spring in the mode where the machine is already running.

## How to apply

- Make the resting position a function of the state the interlock cares about.
  Rest at the end of travel while the interlock is armed; switch to the centre
  detent only once it has been passed.
- Hand the control over explicitly when the regime changes, rather than leaving
  it wherever the previous one had it, and do it in the same step as the state
  change so nothing reads the old rest position in between.
- Write the test as the sequence, not as the two rules: select the mode, then
  immediately try to pass the gate. Testing each rule alone cannot fail.
- The same shape appears wherever a "reset to defaults" leaves a field at a
  value a later validation rejects.
