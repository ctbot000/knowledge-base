---
title: Node's net.BlockList matches a plain IPv4 address against IPv4-mapped IPv6 rules
tags: [node, networking, ipv6, security]
added: 2026-10-09
sources:
  - https://nodejs.org/api/net.html#class-netblocklist
---

## Fact

`net.BlockList` treats an IPv4 address and its IPv4-mapped IPv6 form
(`::ffff:a.b.c.d`) as the same address, in both directions. The documented half:
a rule added for `123.123.123.123` matches a check of `::ffff:7b7b:7b7b`. The
other half: a rule `addSubnet('::ffff:0:0', 96, 'ipv6')` matches **every** plain
IPv4 address checked with `'ipv4'`. Seen on Node 24 and 26.

## Why it matters

A "not public" list built from the IPv6 special-purpose registry usually includes
`::ffff:0:0/96`. With that rule in place, `check('8.8.8.8', 'ipv4')` returns
`true`, so every IPv4 address is classed as private: a filter blocks everything,
or a feature that records public addresses silently records none.

## How to apply

- Leave `::ffff:0:0/96` out of a BlockList. IPv4 rules already cover the mapped
  forms, so mapped private addresses are still caught.
- If mapped addresses must be refused as such, test the string before the list:
  `/^::ffff:/i.test(ip)` (and normalize odd spellings with `new URL` or
  `net.SocketAddress` first if input is untrusted).
- Add a test with one public IPv4 address that must pass; a list that rejects
  everything otherwise looks like it works.
