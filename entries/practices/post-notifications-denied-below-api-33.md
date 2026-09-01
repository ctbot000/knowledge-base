---
title: checkSelfPermission(POST_NOTIFICATIONS) answers DENIED on Android below 13
tags: [android, permissions, notifications]
added: 2026-09-02
---

## Fact

`POST_NOTIFICATIONS` was introduced in API 33. On older releases the platform has
no such permission, so `checkSelfPermission` returns `PERMISSION_DENIED` for it —
even though the app is free to post notifications there and always has been.

## Why it matters

The natural defensive guard, "only notify if the permission is granted", silently
mutes every notification on Android 10 through 12. Nothing throws, nothing logs;
notifications simply never appear, and only on the older devices you are least
likely to be testing on.

## How to apply

Short-circuit the check by version, so it only runs where the permission exists:

```kotlin
val allowed = Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU ||
    ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) ==
        PackageManager.PERMISSION_GRANTED
```

Pair it with `NotificationManagerCompat.areNotificationsEnabled()`, which is the
check that is meaningful on every version — the user can switch notifications off
from settings regardless of API level.
