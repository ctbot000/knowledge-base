---
title: javac rejects an unknown -Xlint key outright, so lint flags are not portable across JDKs
tags: [java, javac, ci]
added: 2026-09-22
sources:
  - https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html
---

## Fact

An unrecognised `-Xlint` key is a hard error — `error: invalid flag:` — not a
warning that javac shrugs off. The key set grows between releases:
`-this-escape` arrived in JDK 21, `serial` and `deprecation` have been there
since forever. A single lint string that suppresses a newer key therefore fails
to compile on an older JDK before a line of source is read.

## Why it matters

It surfaces only when the build matrix widens. A project developed on the latest
JDK compiles cleanly for months, then every older-JDK job in CI dies at
`:compileJava` with a message about a flag rather than about code, so the build
looks broken rather than misconfigured.

## How to apply

Derive the lint keys from the compiling JDK rather than hard-coding them. In a
Gradle build:

```kotlin
tasks.withType<JavaCompile>().configureEach {
    options.release = 17
    val lint = mutableListOf("all", "-serial")
    if (JavaVersion.current().isCompatibleWith(JavaVersion.VERSION_21)) {
        lint += "-this-escape"
    }
    options.compilerArgs.add("-Xlint:" + lint.joinToString(","))
}
```

A fixed Gradle toolchain avoids the problem too, but then the matrix stops
testing what it was added to test.
