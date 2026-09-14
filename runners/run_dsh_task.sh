#!/usr/bin/env bash
set -uo pipefail
ROOT=/home/benchmark-user/benchmarks/flash-agent-bench-20260910
HC="$ROOT/harness_compare_20260911"
TASK="$1"
OUT="$HC/dsh/$TASK"
rm -rf "$OUT"
mkdir -p "$OUT/home" "$OUT/work"
cp -a "$ROOT/base_tasks/$TASK/." "$OUT/work/"
cat > "$OUT/commandcode.patch.yml" <<'YAML'
- id: agent-default-model
  config:
    provider: commandcode
    model: deepseek/deepseek-v4.1-flash
- id: llm-pi-ai
  name: '@deepseek-ai/dsh-llm-pi-ai'
  config:
    providers:
      commandcode:
        displayName: CommandCode
        apiKeyEnv: COMMANDCODE_API_KEY
        api: openai-completions
        baseURL: https://api.commandcode.ai/provider/v1
        reasoning: max
        compat:
          thinkingFormat: deepseek
        defaultContextWindow: 1000000
        defaultMaxTokens: 65536
        models:
          - id: deepseek/deepseek-v4.1-flash
            name: DeepSeek V4.1 Flash
            contextWindow: 1000000
            maxTokens: 65536
            reasoningEfforts:
              off:
              high: high
              max: max
YAML
START=$(date +%s); RC=0
bwrap --ro-bind / / --dev /dev --proc /proc \
  --tmpfs /home/benchmark-user/benchmarks --tmpfs /tmp \
  --dir /tmp/workspace --bind "$OUT/work" /tmp/workspace \
  --dir /tmp/dsh-home --bind "$OUT/home" /tmp/dsh-home \
  --ro-bind "$OUT/commandcode.patch.yml" /tmp/commandcode.patch.yml \
  --chdir /tmp/workspace \
  /bin/bash -lc 'set -a; . /home/benchmark-user/.hermes/.env; set +a; export DSH_HOME=/tmp/dsh-home DSH_TELEMETRY_DISABLED=1 DSH_TELEMETRY_MODE=OFF DSH_PERMISSION_MODE=danger-full-access; exec /home/benchmark-user/.nvm/versions/node/v22.23.0/bin/dsh --profile headless --patch /tmp/commandcode.patch.yml "$(cat /tmp/workspace/task.md)"' \
  > "$OUT/stdout.txt" 2> "$OUT/stderr.txt" || RC=$?
END=$(date +%s)
printf '{"task":"%s","rc":%d,"elapsed_s":%d}\n' "$TASK" "$RC" "$((END-START))" > "$OUT/meta.json"
printf '%s rc=%d elapsed=%ds\n' "$TASK" "$RC" "$((END-START))"
