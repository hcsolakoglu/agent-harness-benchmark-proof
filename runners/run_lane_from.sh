#!/usr/bin/env bash
set -uo pipefail
ROOT=/home/benchmark-user/benchmarks/flash-agent-bench-20260910
MODEL_KEY="$1"
MODEL_ID="$2"
ENGINE="$3"
START_N="${4:-1}"
RUNROOT="/tmp/flashbench_${MODEL_KEY}_resume_$$"
OUT="$ROOT/runs/$MODEL_KEY"
mkdir -p "$RUNROOT" "$OUT/logs" "$OUT/meta"
trap 'rm -rf "$RUNROOT"' EXIT

if [ "$ENGINE" = commandcode ]; then
  STATE="$RUNROOT/state/.commandcode"
  mkdir -p "$(dirname "$STATE")"
  cp -a /home/benchmark-user/.commandcode "$STATE"
  python3 - "$STATE/settings.json" <<'PYCFG'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
d = json.loads(p.read_text())
d.setdefault("permissions", {}).pop("disableBypass", None)
p.write_text(json.dumps(d, separators=(",", ":")))
PYCFG
else
  STATE="$RUNROOT/state/.codex"
  mkdir -p "$STATE"
  cp /home/benchmark-user/.codex/auth.json "$STATE/auth.json"
  [ -f /home/benchmark-user/.codex/installation_id ] && cp /home/benchmark-user/.codex/installation_id "$STATE/installation_id"
fi

for I in $(seq "$START_N" 10); do
  N=$(printf '%02d' "$I")
  TASK="t$N"
  WORK="$RUNROOT/$TASK"
  cp -a "$ROOT/base_tasks/$TASK" "$WORK"
  START=$(date +%s)
  LOG="$OUT/logs/$TASK.jsonl"
  RC=0
  if [ "$ENGINE" = commandcode ]; then
    bwrap --ro-bind / / --dev /dev --proc /proc \
      --tmpfs /home/benchmark-user/benchmarks \
      --bind "$WORK" "$WORK" \
      --bind "$STATE" /home/benchmark-user/.commandcode \
      --chdir "$WORK" \
      /usr/bin/timeout --signal=TERM --kill-after=15s 600 \
      /home/benchmark-user/.nvm/versions/node/v22.23.0/bin/cmd \
      -p "$(cat "$WORK/task.md")" --model "$MODEL_ID" --effort max \
      --output-format json --no-session --max-turns 50 --skip-onboarding \
      --dangerously-skip-permissions --no-skills >"$LOG" 2>&1 || RC=$?
  else
    bwrap --ro-bind / / --dev /dev --proc /proc \
      --tmpfs /home/benchmark-user/benchmarks \
      --bind "$WORK" "$WORK" \
      --bind "$STATE" "$STATE" \
      --chdir "$WORK" \
      /usr/bin/env CODEX_HOME="$STATE" \
      /usr/bin/timeout --signal=TERM --kill-after=15s 600 \
      /home/benchmark-user/.local/bin/codex exec -m "$MODEL_ID" \
      -c 'model_reasoning_effort="max"' --ignore-user-config --ignore-rules \
      --ephemeral --dangerously-bypass-approvals-and-sandbox \
      --disable apps --disable plugins --disable browser_use --disable computer_use \
      --disable image_generation --disable skill_search --disable multi_agent \
      --json "$(cat "$WORK/task.md")" >"$LOG" 2>&1 || RC=$?
  fi
  END=$(date +%s)
  printf '{"task":"%s","exit_code":%d,"elapsed_s":%d}\n' "$TASK" "$RC" "$((END-START))" > "$OUT/meta/$TASK.json"
  rm -rf "$OUT/$TASK"
  cp -a "$WORK" "$OUT/$TASK"
  printf '%s %s rc=%s elapsed=%ss\n' "$MODEL_KEY" "$TASK" "$RC" "$((END-START))"
done
