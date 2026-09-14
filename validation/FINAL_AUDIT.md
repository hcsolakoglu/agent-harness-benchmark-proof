# Final publication audit

- Gitleaks final scan: 0 findings across ~61.6 MB.
- Independent PII/credential regex scan: 0 findings.
- Frozen candidate implementation byte identity: 50/50.
- eval_v3 core evaluator byte identity: 10/10.
- Sanitized trace structural preservation: 50/50.
- Reproduced eval_v3 hard passes: Luna 10/10; GLM 8/10; direct DeepSeek V4.1 7/10; Hermes DeepSeek V4.1 7/10; DeepSeek Harness DeepSeek V4.1 9/10.
- Raw traces, auth homes, environment files, state databases, caches, keyrings, and smoke runtime state are excluded.
- Trace correlation IDs are pseudonymized; raw local usernames/home paths, emails, IPs, UUID/session IDs, and common credential formats are redacted.

Residual limitation: automated scanning substantially reduces disclosure risk but cannot mathematically prove absence of every possible sensitive string. The export uses an allowlist rather than copying the raw benchmark tree wholesale.
