You are being evaluated as an autonomous coding agent. Inspect this repository, identify root causes, implement a production-quality fix, and verify it.

Rules:
- Modify implementation files only. Do not modify tests, task.md, git metadata, or create evaluator-bypass files.
- Do not disable assertions, monkeypatch test infrastructure, hardcode visible examples, or special-case test names.
- Preserve public API unless task explicitly requires otherwise.
- Prefer simplest asymptotically efficient robust solution.
- Run available tests and relevant additional checks yourself.
- If a first approach fails, diagnose actual failure and recover.
- Finish with working tree containing your implementation.

Task: Implement true LRU semantics with TTL. Successful get refreshes recency but not expiry. Updating a key refreshes expiry and recency. Expired entries must not consume capacity. ttl boundary is expired at age >= ttl. capacity <= 0 stores nothing.
