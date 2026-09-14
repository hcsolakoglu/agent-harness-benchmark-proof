# Agent Harness Benchmark Proof

Private proof package for the 10-task coding-agent benchmark run on 2026-09-10/11. It contains frozen tasks, evaluator versions, frozen candidate implementations, result reports, and sanitized traces for five evaluated lanes.

## Final strong evaluator (eval_v3)

| Lane | Hard passes |
|---|---:|
| GPT-5.6 Luna Max / Codex CLI | 10/10 |
| DeepSeek V4.1 Flash / DeepSeek Harness / CommandCode | 9/10 |
| GLM-5.3 Flash / CommandCode | 8/10 |
| DeepSeek V4.1 Flash / Hermes / CommandCode | 7/10 |
| DeepSeek V4.1 Flash / direct CommandCode | 7/10 |

## Benchmark visibility

Agents could see `task.md`, implementation source, and `test_public.py`. Hidden evaluator files were outside the agent-visible benchmark mount and were applied after each agent run. `eval_v3` was created after the original candidate runs and was applied to the frozen candidate outputs; Luna, GLM, and direct DeepSeek were not regenerated specifically for eval_v3.

## Trace integrity and privacy

`traces/` contains sanitized copies only. Raw traces remain local and are not committed. Redactions cover local account identifiers/paths, email addresses, IP addresses, UUID/session identifiers, and common credential/token formats. `manifests/redaction_manifest.json` records source and sanitized SHA-256 values plus redaction counts without storing redacted values.

Runtime home directories, auth files, state databases, caches, smoke sessions, and provider credentials are intentionally excluded.

## Important interpretation caveats

This benchmark used one stochastic run per lane, so harness differences are strong observations rather than causal proof. Public tests were visible, while final/hidden evaluator cases were not. Once evaluator contents are shared with someone, they should no longer be treated as unseen holdout tests for that person.

See `SANITIZATION.md` and `results/` for details.
