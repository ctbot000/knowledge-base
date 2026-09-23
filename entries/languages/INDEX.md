# languages

- [GLSL rejects a long list of words it does not implement, and `half` is one of them](glsl-reserved-words.md) — Reserved-for-future-use identifiers are compile errors, and `half` is the natural name for a Blinn-Phong halfway vector. `glsl`, `webgl`, `shaders`
- [Node's strict assertions fail -0 against 0](assert-strict-rejects-negative-zero.md) — `Object.is` separates them, so a `-0` out of a sign flip *or* any multiply or divide that lands on zero fails a check that `===` would pass — `deepEqual` included. `javascript`, `testing`, `numerics`
- [asyncio's Server.wait_closed() waits for live connections, not just the listener](asyncio-wait-closed-waits-for-connections.md) — Since Python 3.12 it blocks until every handler ends, so awaiting it before telling clients to leave deadlocks. `python`, `asyncio`, `shutdown`
- [Math.max cannot floor a NaN, so a clamped loop bound can still run zero times](math-max-cannot-floor-nan.md) — `Math.max(1, NaN)` is NaN, so the loop runs zero times while the `!== 0` liveness test keeps reporting the entity as moving. `javascript`, `numerics`, `simulation`
- [An inherited member type shadows a single-type import of the same name](inherited-nested-type-beats-import.md) — The compiler then reports the imported class's own methods as missing, and only the classes implementing that interface are affected. `java`, `scoping`, `imports`
