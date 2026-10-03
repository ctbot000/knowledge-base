---
title: A NAT64 address has to be classified by the IPv4 address it embeds
tags: [networking, ipv6, nat64, security]
added: 2026-10-03
sources:
  - https://www.rfc-editor.org/rfc/rfc6052
  - https://www.rfc-editor.org/rfc/rfc7050
  - https://www.rfc-editor.org/rfc/rfc8215
  - https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml
---

## Fact

On a DNS64/NAT64 network, common on mobile carriers and phone hotspots, an AAAA
lookup for an IPv4-only host returns a synthesized address in `64:ff9b::/96` with
the real IPv4 address in the low 32 bits: `192.0.2.33` comes back as
`64:ff9b::c000:221`. Clients usually prefer it, so it is the address a connection
actually goes to.

## Why it matters

An IP-range check that does not decode the prefix fails one of two ways. Treat
`64:ff9b::/96` as non-public and every IPv4-only site looks like it is on a private
network (prompts, or requests blocked outright), but only on that network, so it
reads as the site being broken. Treat it as public and `64:ff9b::7f00:1`
(127.0.0.1) or `64:ff9b::a00:1` (10.0.0.1) passes a private-address filter: an SSRF
hole.

## How to apply

- Confirm the network does NAT64: `dig +short AAAA ipv4only.arpa` returns
  `64:ff9b::c000:aa` (RFC 7050) instead of nothing.
- In a check, take the last 32 bits of a `64:ff9b::/96` address and classify that
  IPv4 address. Treat `64:ff9b:1::/48`, the local-use translation prefix
  (RFC 8215), as private.
- When a site fails or warns only on a hotspot or carrier network, look at its
  AAAA answer before blaming the site.
