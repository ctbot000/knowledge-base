---
title: An inherited member type shadows a single-type import of the same name
tags: [java, scoping, imports]
added: 2026-09-22
sources:
  - https://docs.oracle.com/javase/specs/jls/se21/html/jls-6.html#jls-6.5.5
---

## Fact

In Java, a member type inherited from a superclass or an implemented interface
takes precedence over a single-type import with the same simple name. A class
that implements `Renderer`, where `Renderer` declares a nested `Format`, resolves
every bare `Format` inside that class to `Renderer.Format` — even with
`import com.example.util.Format;` at the top of the file.

## Why it matters

The failure looks nothing like a name clash. The compiler reports
`cannot find symbol: method timestamp(Instant)` on the imported class's own
methods, because it is looking them up on the inherited nested type instead. The
import sits there unused and blameless, and only the classes that implement the
interface are affected — its siblings compile fine, which points suspicion at the
utility class rather than at the interface.

## How to apply

- Do not give a nested type in an interface a name that a widely imported class
  already uses. Enum names like `Format`, `Type`, `Kind`, `State` and `Entry` are
  the usual collisions.
- Prefer a top-level enum to a nested one when the interface has many
  implementors and the name is generic.
- When the error insists a method is missing from a class you can see declaring
  it, print the resolved type: `Format.class.getName()` names the winner
  immediately, and a fully qualified reference confirms the diagnosis.
