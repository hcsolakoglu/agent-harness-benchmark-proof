# Flash Agent Benchmark Re-audit — 2026-09-11

## Scope
Re-audited all 30 raw model traces, implementation diffs, original public/hidden evaluators, plus a new frozen audit-v2 evaluator. Luna t05 original trace was provenance-contaminated by a vanished workspace, so it was rerun cleanly under the same frozen task/model/harness; original artifact was preserved.

## Final rubric
Each task is scored 0–5 on:
1. Functional correctness
2. Spec/edge-case completeness
3. Root-cause diagnosis
4. Algorithmic efficiency
5. Failure-path robustness
6. Verification quality
7. Recovery from mistakes/tool failures
8. Maintainability/minimality
9. Task discipline/integrity
10. Agent efficiency/decisiveness

5 = excellent/no material issue; 4 = strong/minor issue; 3 = acceptable but meaningful limitation; 2 = substantial issue; 1 = poor; 0 = task requirement effectively not implemented. Hard deterministic failures are reported separately and are not hidden by aggregate scores.

## Final aggregate
- GPT-5.6 Luna Max: 472.5/500 (4.725/5)
- GLM-5.3 Flash: 445.5/500 (4.455/5)
- DeepSeek V4.1 Flash: 429.5/500 (4.295/5)

## Criterion averages
| Criterion | Luna | GLM | DeepSeek |
|---|---:|---:|---:|
| Correctness | 5.00 | 4.75 | 4.30 |
| Spec completeness | 5.00 | 4.70 | 4.20 |
| Root-cause diagnosis | 5.00 | 5.00 | 4.90 |
| Algorithmic efficiency | 4.35 | 4.75 | 4.45 |
| Failure robustness | 4.90 | 4.50 | 4.20 |
| Verification quality | 4.70 | 4.50 | 4.10 |
| Recovery | 4.90 | 4.50 | 4.25 |
| Maintainability | 4.45 | 4.35 | 4.00 |
| Discipline/integrity | 5.00 | 4.45 | 4.55 |
| Agent efficiency | 3.95 | 3.05 | 4.00 |

## Task totals (/50)
| Task | Luna | GLM | DeepSeek |
|---|---:|---:|---:|
| t01 intervals | 49.0 | 47.0 | 48.0 |
| t02 JSONL stream | 43.5 | 46.5 | 48.0 |
| t03 LRU+TTL | 42.0 | 41.5 | 47.5 |
| t04 topo scheduler | 48.5 | 48.0 | 46.5 |
| t05 retry | 49.5 | 47.5 | 48.0 |
| t06 safe_join | 48.0 | 38.5 | 13.5 |
| t07 bounded async map | 47.0 | 46.5 | 44.5 |
| t08 SemVer | 47.0 | 37.5 | 39.5 |
| t09 unique substring | 49.5 | 48.0 | 48.5 |
| t10 atomic ledger | 48.5 | 44.5 | 45.0 |

## Important findings
- Luna remained 10/10 on both original hidden and audit-v2 hard correctness gates. Its main weaknesses are performance, not semantics: t02 bytearray front-deletion/copy behavior scales badly under byte-at-a-time long records; t03 purges the entire cache on every get/put, making repeated hits O(n^2) in aggregate.
- GLM is often algorithmically stronger than Luna. t03 is very fast, but its expiry heap accumulates stale entries on repeated updates (5000 live entries -> heap 25000 after 20000 updates with long TTL), creating unbounded memory growth until expiry cleanup. t06 exposes raw RuntimeError on a symlink loop rather than ValueError and left verify_t06.py despite implementation-only rules. t08 raises TypeError for non-string invalid versions and fails valid >4300-digit SemVer numeric identifiers due Python int conversion limits.
- DeepSeek is usually fast and diagnoses root causes well, but t06 is a true hard failure: no implementation patch was persisted and the baseline accepts traversal, absolute paths, root aliases and symlink escapes. t08 accepts a Unicode digit in a SemVer numeric component and fails >4300-digit valid numeric identifiers. t10 has a minor malformed-op exception-contract gap (`None` entry -> TypeError). Its t07 solution is capable but over-engineered and went through multiple self-inflicted edit/test errors before recovery.

## Harness caveat
This benchmark measures model + agent harness, not pure model intelligence: Luna ran through Codex while DeepSeek/GLM ran through CommandCode. Cleanup permission behavior and trace verbosity are therefore partly harness effects. Correctness and independent evaluator results are more comparable than latency/tool-count metrics.
