# hidden_eval_v2

Versioned replacement for the original hidden evaluator. The original `hidden_eval/` is intentionally preserved so historical results remain reproducible.

Current correction:

- `t04_hidden.py`: accepts any `ValueError` for a cycle. The frozen task requires the exception type, not any particular wording. The old evaluator incorrectly required the literal substring `cycle` and therefore rejected valid messages such as `cyclic dependencies detected`.

For stronger final adjudication use `audit_20260911/eval_v3/`, which covers more edge cases while keeping non-contract diagnostics separate from hard failures.
