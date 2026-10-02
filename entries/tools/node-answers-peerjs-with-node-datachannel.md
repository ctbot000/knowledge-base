---
title: A Node process can answer PeerJS browser peers with node-datachannel and the PeerServer protocol written by hand
tags: [peerjs, webrtc, node, signaling]
added: 2026-10-03
sources:
  - https://github.com/peers/peerjs/blob/master/lib/negotiator.ts
  - https://github.com/peers/peerjs-server/blob/master/src/enums.ts
  - https://github.com/murat-dogan/node-datachannel
---

## Fact

A server can be a PeerJS data peer without the PeerJS client or a browser:
open the PeerServer WebSocket itself and answer offers with node-datachannel,
which ships prebuilt binaries as per-platform optional dependencies (no
compiler, no install script). Browsers using PeerJS 1.5 cannot tell it apart
from another browser, and Chrome's default mDNS-hidden host candidates still
connect.

## Why it matters

It lets an always-on machine (a home server, a bot, a store-and-forward
service) join a peer-to-peer app under a fixed id, with no open ports, tunnel
or HTTPS certificate, reusing the app's signaling and TURN servers.

## How to apply

- Connect `wss://host:port/<path>peerjs?key=peerjs&id=<id>&token=<random>`
  (the cloud is `0.peerjs.com:443`, path `/`). Send `{"type":"HEARTBEAT"}`
  every 5 s. `OPEN` means registered; `ID-TAKEN` means try again later.
- A dial arrives as `OFFER` with `src` and `payload: { sdp: { type, sdp },
  type: "data", connectionId, label, serialization, reliable }`. Create
  `new PeerConnection(connectionId, { iceServers })`, call
  `setRemoteDescription(payload.sdp.sdp, "offer")`, and send what the callbacks
  produce, with `dst: src`:
  - `onLocalDescription(sdp, type)` → `ANSWER`, `payload: { sdp: { type, sdp },
    type: "data", connectionId }`
  - `onLocalCandidate(candidate, mid)` → `CANDIDATE`, `payload: { candidate:
    { candidate, sdpMid: mid, sdpMLineIndex: 0 }, type: "data", connectionId }`
- Feed incoming `CANDIDATE` payloads to `addRemoteCandidate(c.candidate,
  c.sdpMid)`. The browser opened the channel; it arrives in `onDataChannel`.
- With `serialization: "raw"` the channel carries the page's strings as they
  are; chunk long ones yourself, as in the browser.
