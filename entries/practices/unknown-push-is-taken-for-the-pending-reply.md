---
title: Where replies carry no ids, a push an older client does not know is taken for the reply it is waiting for
tags: [protocols, networking, api-design, deployment, compatibility]
added: 2026-11-25
---

## Fact

On a channel where requests are answered one at a time and in order, with no
id tying a reply to its request, a client reads the next message as the answer
to whatever it asked. A new kind of unsolicited message ("something changed on
your other device") is therefore not ignored by a client from before it: it is
consumed as that answer, and the real answer then arrives with nothing waiting.

## Why it matters

Clients stay open across a deploy, so a server that starts pushing breaks pages
that were working a minute before. Nothing looks wrong on the server, and the
symptom on the client is in whatever it happened to be asking: a save treated
as refused, a list treated as empty, every later reply one off.

## How to apply

- Have the client declare what pushes it understands as it connects (a flag per
  kind, or a protocol version), and push only what was declared. Adding the
  flag and the push in one release is enough.
- On the client, sort out known pushes by kind before matching a reply, and
  drop unknown kinds instead of treating them as replies.
- When the protocol is yours to change, give requests ids and echo them: then
  an unknown push matches nothing and is harmless.
- Test with a connection that does not declare the flag while another one of
  the same user causes the push.
