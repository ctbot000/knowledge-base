---
title: A WebRTC peer's real address comes from the selected candidate pair, not from the candidates it signals
tags: [webrtc, networking, node]
added: 2026-10-09
sources:
  - https://www.rfc-editor.org/rfc/rfc8445#section-7.3.1.3
  - https://datatracker.ietf.org/doc/html/draft-ietf-mmusic-mdns-ice-candidates
---

## Fact

Browsers signal private host addresses only as mDNS names (`<uuid>.local`), and
a page's STUN (srflx) candidate is not guaranteed to be signaled at all: Chrome
was seen finishing gathering with only the two mDNS host candidates while the
same machine got a srflx candidate from the same STUN server in a bare test. The
connection still works, because the other side learns the page's address as a
peer-reflexive candidate from its connectivity checks, and that never travels
through signaling.

## Why it matters

A server that records "where a peer is" by parsing signaled candidates records
nothing for some peers, intermittently, with no error. Peers on the server's own
LAN are never seen at all.

## How to apply

- Read the selected pair once the ICE state is `connected`: in node-datachannel,
  `pc.getSelectedCandidatePair().remote.address` (type `host`, `prflx`, `srflx`
  or `relay`); in browsers, `RTCIceTransport.getSelectedCandidatePair()` or the
  `candidate-pair` stats entry.
- Skip `relay`: that address is the TURN server's.
- Keep signaled srflx candidates as a fallback, and treat a private pair address
  as "same network as me", not as a location.
