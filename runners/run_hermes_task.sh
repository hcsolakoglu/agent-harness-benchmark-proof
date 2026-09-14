#!/usr/bin/env bash
set -uo pipefail
ROOT=/home/benchmark-user/benchmarks/flash-agent-bench-20260910
HC="$ROOT/harness_compare_20260911"
TASK="$1"
OUT="$HC/hermes/$TASK"
rm -rf "$OUT"
mkdir -p "$OUT/home" "$OUT/work"
cp -a "$ROOT/base_tasks/$TASK/." "$OUT/work/"
cat > "$OUT/home/config.yaml" <<'YAML'
model:
  default: deepseek/deepseek-v4.1-flash
  provider: commandcode
  api_mode: chat_completions
model_overrides:
  commandcode:
    deepseek/deepseek-v4.1-flash:
      context_window: 1000000
toolsets: [terminal, file]
agent:
  reasoning_effort: max
  verbose: false
  task_completion_guidance: true
  environment_probe: true
terminal:
  backend: local
  cwd: /tmp/workspace
  timeout: 600
YAML
START=$(date +%s); RC=0
bwrap --ro-bind / / --dev /dev --proc /proc \
  --tmpfs /home/benchmark-user/benchmarks --tmpfs /tmp \
  --dir /tmp/workspace --bind "$OUT/work" /tmp/workspace \
  --dir /tmp/hermes-home --bind "$OUT/home" /tmp/hermes-home \
  --chdir /tmp/workspace \
  /bin/bash -lc 'set -a; . /home/benchmark-user/.hermes/.env; set +a; export HERMES_HOME=/tmp/hermes-home; exec /home/benchmark-user/.local/bin/hermes --in /tmp/workspace -z "$(cat /tmp/workspace/task.md)" -m deepseek/deepseek-v4.1-flash --provider commandcode --reasoning max -t terminal,file --ignore-rules --yolo --usage-file /tmp/hermes-home/usage.json' \
  > "$OUT/stdout.txt" 2> "$OUT/stderr.txt" || RC=$?
END=$(date +%s)
printf '{"task":"%s","rc":%d,"elapsed_s":%d}\n' "$TASK" "$RC" "$((END-START))" > "$OUT/meta.json"
printf '%s rc=%d elapsed=%ds\n' "$TASK" "$RC" "$((END-START))"
