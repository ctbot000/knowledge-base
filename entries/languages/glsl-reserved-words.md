---
title: GLSL rejects a long list of words it does not implement, and `half` is one of them
tags: [glsl, webgl, shaders]
added: 2026-09-11
sources:
  - https://registry.khronos.org/OpenGL/specs/es/2.0/GLSL_ES_Specification_1.00.pdf
---

## Fact

GLSL reserves a set of identifiers "for future use" that are not keywords in the
language you are actually writing. Using one is a compile error, not a warning:

```
ERROR: 0:20: 'half' : Illegal use of reserved word
```

The list is long and contains ordinary nouns — in GLSL ES 1.00 it includes
`half`, `double`, `long`, `short`, `input`, `output`, `interface`, `union`,
`this`, `namespace`, `switch`, `default`, `goto`, and the `hvec`/`fvec`/`dvec`
vector families. Several are the obvious name for the thing being computed.
`half` is the one that bites hardest, because the Blinn-Phong halfway vector is
called the half vector in every text that describes it:

```glsl
vec3 half = normalize(lightDir + viewDir);   // will not compile
```

## Why it matters

Shader compilation failures are reported through the API rather than thrown, so
whatever the program does when the shader fails is what you see. Code that falls
back — to a second renderer, to a flat colour, to a 2D path — swallows the error
entirely and the feature is simply absent, with the real message sitting in a
`getShaderInfoLog` nobody read.

When the message is read, it is still misleading if the identifier is not a
keyword in any language you know. Nothing about `half` looks reserved, so the
first guess is a typo or a driver quirk rather than the spec.

## How to apply

- Always read `getShaderInfoLog` on failure and surface it. One `console.warn`
  turns this from a mystery into a one-line fix.
- Suspect the reserved list whenever a shader rejects an identifier that is not
  a keyword in the language. Rename rather than investigating the driver.
- Prefer a qualified name — `halfway`, `halfVector` — over the bare noun; it is
  free and it survives a future spec revision that reserves more words.
