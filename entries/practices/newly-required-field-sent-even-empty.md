---
title: A request field a server starts checking should be sent by every new client, even empty, so that its absence marks an outdated one
tags: [protocols, api-design, deployment, clients]
added: 2026-11-17
---

## Fact

When a server starts refusing requests that lack something (a ticket, a
licence, a consent flag), new clients should always send the field, as an
empty list or `false` when they hold nothing. Then a request without the
field at all can only come from a client built before the check, and the
server can tell it apart from one that genuinely lacks the thing.

## Why it matters

Clients stay open across a deploy: a tab, a game left running on a tablet,
an app not yet updated. If new clients omit the field when it is empty, the
server cannot distinguish them from old ones, and an old client is refused
with the message meant for someone who lacks the thing ("you need a ticket"),
although after a reload it may well hold one. The user acts on the wrong
message, and nothing in the logs looks wrong.

## How to apply

- Always serialise the field from the release that introduces the check:
  `{ tickets: [] }`, never `{}` for "none".
- On the server, branch on presence before content: absent → "please
  update/reload"; present but insufficient → the real refusal.
- Treat a malformed value (wrong type) like absence, not like an empty one,
  unless a tampered client must be told the real reason.
- Test both refusals separately, and test that every request path a current
  client uses (first join, reconnect, side requests) carries the field.
