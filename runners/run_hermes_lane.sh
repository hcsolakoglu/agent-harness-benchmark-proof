#!/usr/bin/env bash
set -uo pipefail
HC=/home/benchmark-user/benchmarks/flash-agent-bench-20260910/harness_compare_20260911
mkdir -p "$HC/hermes"
# Keep provider contention moderate while still parallelizing.
printf '%s\n' t01 t02 t03 t04 t05 t06 t07 t08 t09 t10 | xargs -n1 -P3 "$HC/run_hermes_task.sh"
