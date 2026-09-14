#!/usr/bin/env bash
set -uo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 CANDIDATE_TASK_ROOT" >&2; exit 2; fi
EVAL_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CROOT=$1
fail=0
for i in $(seq 1 10); do n=$(printf '%02d' "$i"); C="$CROOT/t$n"; [ -d "$C/work" ] && C="$C/work"; rc=0; out=$(PYTHONDONTWRITEBYTECODE=1 timeout 20 python3 "$EVAL_DIR/t$n.py" "$C" 2>&1) || rc=$?; printf 't%s rc=%d %s\n' "$n" "$rc" "$(echo "$out" | tr '\n' ' ' | head -c 1500)"; [ "$rc" -eq 0 ] || fail=1; done
exit "$fail"
