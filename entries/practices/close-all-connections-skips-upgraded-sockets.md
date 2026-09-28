---
title: http.Server.closeAllConnections() does not close upgraded connections, so server.close() waits on every open WebSocket
tags: [node, http, websocket, testing]
added: 2026-09-28
sources:
  - https://nodejs.org/api/http.html#servercloseallconnections
  - https://nodejs.org/api/net.html#serverclosecallback
---

## Fact

After an HTTP upgrade, the socket leaves the HTTP server's own connection
tracking but still counts for the underlying `net.Server`.
`closeAllConnections()` skips it, and the `server.close()` callback does not
fire until every upgraded socket, typically a WebSocket, has ended by itself.
Checked on Node 26.

## Why it matters

The usual test teardown, `close()` plus `closeAllConnections()`, hangs as soon
as a test opened a WebSocket, which is exactly when it exercises a real-time
server. The run waits for the runner's timeout or a force exit. A test that
stops the server to simulate an outage is quietly wrong too: clients stay
connected to the old instance, so no outage happens.

## How to apply

- Track raw sockets and destroy them on teardown:

  ```js
  const sockets = new Set();
  server.on('connection', (s) => { sockets.add(s); s.on('close', () => sockets.delete(s)); });
  // teardown
  const closed = new Promise((resolve) => server.close(resolve));
  for (const s of sockets) s.destroy();
  await closed;
  ```

- With the `ws` library, `wss.clients.forEach((client) => client.terminate())`
  covers its own sockets.
