# DeepSeek V4.1 Flash Harness Re-evaluation

## Evaluator corrections

Two versioned evaluator layers are now authoritative for new comparisons:

- `hidden_eval_v2/`: preserves the original hidden suite except the confirmed t04 false negative. A cycle only needs to raise `ValueError`; exception wording is not part of the frozen task contract.
- `audit_20260911/eval_v3/`: stronger final adjudication suite. It separates hard task-contract checks from useful but non-contract diagnostics.

Original `hidden_eval/` and `eval_v2/` remain unchanged for provenance.

Important v3 fixes include: portable t03 performance/memory diagnostics without private-attribute assumptions; corrected t04 exception contract; bounded local timeouts and a valid source-failure setup for t07; symlink-loop behavior in t06 made diagnostic because a non-escaping loop is not specified by the frozen task; machine-sensitive t02 scaling retained as a metric rather than a hard threshold.

## Hard results

| Lane | hidden_eval_v2 | eval_v3 |
|---|---:|---:|
| GPT-5.6 Luna Max | 10/10 | 10/10 |
| GLM-5.3 Flash | 10/10 | 8/10 |
| DSV4.1 direct CommandCode | 9/10 | 7/10 |
| DSV4.1 Hermes + CommandCode | 9/10 | 7/10 |
| DSV4.1 DeepSeek Harness + CommandCode | 10/10 | 9/10 |

DSH's only hard v3 failure is t08: valid SemVer numeric identifiers longer than Python's configured `int()` decimal conversion limit fail. This is a real SemVer robustness/spec issue, not an evaluator artifact.

Hermes hard v3 failures are t01, t06 and t08. Direct DSV4.1 hard failures are t06, t08 and t10.

## DSV harness rubric

The 500-point rubric remains a manual quality score; hard evaluator passes are the primary objective signal. Same ten dimensions as the prior audit were used: functional correctness, spec completeness, root-cause diagnosis, algorithmic efficiency, failure robustness, verification quality, recovery, maintainability/minimality, task discipline/integrity, and agent efficiency/decisiveness.

| Task | Direct | Hermes | DSH |
|---|---:|---:|---:|
| t01 interval union | 48 | 35 | 48 |
| t02 streaming JSONL | 48 | 44 | 45 |
| t03 TTL LRU | 47.5 | 48 | 42 |
| t04 scheduler | 46.5 | 47 | 46 |
| t05 retry | 48 | 48 | 48 |
| t06 safe path | 13.5 | 39 | 44 |
| t07 bounded async map | 44.5 | 44 | 43 |
| t08 SemVer | 39.5 | 37 | 40 |
| t09 unique window | 48.5 | 49 | 46 |
| t10 ledger | 45 | 48 | 48 |
| **Total** | **429.5/500** | **439/500** | **450/500** |

The DSH score is deliberately held down for very high execution cost and over-engineering even though its correctness rate is best. Hermes gains over direct mostly by eliminating execution/harness failure on t06 and tightening t10, but loses t01 through a wrong semantic decision.

## Performance / harness behavior

Approximate sum of per-task wall times (not a perfectly controlled provider-latency benchmark):

- direct CommandCode: ~594 s
- Hermes: 437 s
- DSH: 1,245 s

DSH is therefore about 2.85x Hermes task-time sum in this run. Much of the difference comes from t03 (308 s), t06 (291 s), and t07 (183 s). Full DSH traces show 43 steps on t03 and 41 on t06, with several self-authored test/oracle failures that the agent diagnosed and recovered from.

DSH full traces for all ten tasks were decompressed and every JSON event parsed. No hidden/evaluator leakage was found, and `task.md` / `test_public.py` hashes stayed unchanged. DSH request metadata confirms `provider=commandcode`, `model=deepseek/deepseek-v4.1-flash`, `reasoningEffort=max`, and 1,000,000 context configuration.

## Important implementation findings

- **t01:** Hermes interprets reversed `[a,b)` with `a>b` as empty. This contradicts the benchmark's intended endpoint-normalization semantics and fails both hidden/v3. DSH correctly inferred intended behavior and passes.
- **t03:** Hermes and direct DSV4.1 are extremely fast and memory-stable. DSH is also fast at runtime and explicitly compacts stale expiry heap records, but spent far longer reasoning/testing. GLM remains fast but its hot-update heap grows materially in the diagnostic.
- **t06:** Direct DSV4.1 never persisted a patch. Hermes produces a mostly correct solution but accepts interior parent traversal such as `a/../b`, contrary to explicit `Reject ... parent traversal`. DSH rejects traversal, absolute paths, root itself, dangling outward symlinks, and outward symlink escapes. Its self-loop is accepted; this is now a diagnostic, not a hard failure, because the loop does not escape root and the task does not define loop semantics.
- **t07:** audit-v2's source-failure test was invalid: it blocked the first two jobs and expected a lazy bounded producer to request item three. v3 fixes this. Hermes and DSH both pass. Their ordered-window design can delay observing a later task's failure until an earlier result completes; this is a robustness/latency consideration, not a frozen-contract failure.
- **t08:** DSH is otherwise strict and handles ASCII SemVer grammar correctly, but converts numeric identifiers with Python `int()`, so very large valid identifiers fail. Luna remains the strongest t08 solution.
- **t10:** strict `plain integer` is treated as `type(amount) is int`, so bool and custom int subclasses are rejected. Hermes and DSH pass; direct DSV4.1 and GLM do not.

## Conclusion

For DeepSeek V4.1 Flash on this suite:

1. **DeepSeek Harness + CommandCode** gives the highest reliability/correctness: 9/10 on the stronger evaluator, 450/500 manual rubric.
2. **Hermes + CommandCode** is the better speed/reliability compromise: much faster than DSH and fixes the direct harness's catastrophic t06 execution failure, but this run introduced semantic regressions on t01/t08 and incomplete traversal policy on t06.
3. **Direct CommandCode CLI** remains the fastest/minimal route but has the weakest autonomous execution reliability in this sample.

Harness choice materially changes observed model capability. Results should therefore be labeled by the full model + harness + provider tuple rather than treated as a harness-independent model score.
