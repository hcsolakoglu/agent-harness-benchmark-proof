# Evaluator v3

This evaluator supersedes audit-v2 for final adjudication. Original evaluator files are retained unchanged for provenance.

Hard checks are limited to the frozen task contract. Performance and non-required robustness properties are emitted as diagnostics unless the task explicitly requires scalability.

Key fixes:

- t01 keeps intended reversed-endpoint normalization but uses an independent brute-force oracle on bounded coordinates.
- t02 keeps correctness hard; bytewise scaling is reported as a metric rather than imposing a machine-sensitive threshold.
- t03 adds stronger semantic coverage and portable time/memory diagnostics without inspecting private attribute names.
- t04 removes the erroneous requirement that a ValueError message literally contain `cycle`.
- t05 strengthens exact retry count, delays, exception identity, and non-transient propagation.
- t06 keeps explicit parent-traversal rejection hard. Symlink-loop behavior is diagnostic because the frozen task requires symlink escapes to be rejected but does not specify behavior or exception type for a non-escaping loop.
- t07 fixes the source-failure test: a lazy bounded implementation is no longer expected to pull a third item while its first two calls are deliberately blocked. Every async failure/cancellation case has a local timeout so a candidate bug cannot hang the evaluator indefinitely. Laziness allows a finite bounded prefetch rather than requiring exactly `limit` source pulls.
- t08 retains SemVer 2.0 validation, ASCII grammar, ValueError contract, and arbitrary-length numeric identifiers.
- t09 retains exact earliest-tie oracle and scalable 500k-character check with a more generous runtime bound.
- t10 retains strict `plain integer` meaning (`type(x) is int`), malformed-op atomicity, and generator late-failure atomicity.
