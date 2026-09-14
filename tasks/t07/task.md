You are being evaluated as an autonomous coding agent. Inspect this repository, identify root causes, implement a production-quality fix, and verify it.

Rules:
- Modify implementation files only. Do not modify tests, task.md, git metadata, or create evaluator-bypass files.
- Do not disable assertions, monkeypatch test infrastructure, hardcode visible examples, or special-case test names.
- Preserve public API unless task explicitly requires otherwise.
- Prefer simplest asymptotically efficient robust solution.
- Run available tests and relevant additional checks yourself.
- If a first approach fails, diagnose actual failure and recover.
- Finish with working tree containing your implementation.

Task: bounded_map must run async fn concurrently with at most limit in flight, preserve input result order, work with any iterable, and reject limit < 1. Avoid eagerly creating unbounded tasks for huge iterables.
