---
title: Android Gradle Plugin 9 applies Kotlin itself and fails if you also apply the Kotlin plugin
tags: [android, gradle, kotlin]
added: 2026-09-02
sources:
  - https://kotl.in/gradle/agp-built-in-kotlin
---

## Fact

From AGP 9.0 the Android plugin has built-in Kotlin support. Applying
`org.jetbrains.kotlin.android` next to it is not merely redundant — the build
fails outright with "The 'org.jetbrains.kotlin.android' plugin is no longer
required for Kotlin support since AGP 9.0".

The Compose compiler plugin is a separate concern and is still applied by hand.

## Why it matters

Every Android/Kotlin project written before AGP 9 declares that plugin, and every
tutorial still shows it. The failure lands at plugin-application time, before any
of your code is compiled, so it looks like a broken toolchain rather than a
two-line config change.

## How to apply

When moving to AGP 9, drop `org.jetbrains.kotlin.android` from the module and from
the root `plugins {}` block, and keep `org.jetbrains.kotlin.plugin.compose` if the
project uses Compose. Set the JVM target through the `kotlin` extension rather
than the removed `android.kotlinOptions`:

```kotlin
kotlin {
    compilerOptions {
        jvmTarget = JvmTarget.JVM_17
    }
}
```

Recent AndroidX releases pull the other way: they require AGP 9.1+ and a
`compileSdk` newer than AGP 8 will accept, so the upgrade is usually forced by a
dependency bump rather than chosen.
