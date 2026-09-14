You are being evaluated as an autonomous coding agent. Inspect this repository, identify root causes, implement a production-quality fix, and verify it.

Rules:
- Modify implementation files only. Do not modify tests, task.md, git metadata, or create evaluator-bypass files.
- Do not disable assertions, monkeypatch test infrastructure, hardcode visible examples, or special-case test names.
- Preserve public API unless task explicitly requires otherwise.
- Prefer simplest asymptotically efficient robust solution.
- Run available tests and relevant additional checks yourself.
- If a first approach fails, diagnose actual failure and recover.
- Finish with working tree containing your implementation.

Task: JsonlStream.feed receives arbitrary byte chunks from a network stream and must emit only complete JSONL records. UTF-8 codepoints and JSON records may cross chunk boundaries. Blank lines are ignored.
