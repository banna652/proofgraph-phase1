#!/usr/bin/env bash
set -euo pipefail

TOKEN="${INGEST_TOKEN:-devtoken}"

echo "[1] reset output files"
rm -f proofgraph/output/proof.json proofgraph/output/state.json || true
python -c "from proofgraph.core.state import save_state, SourceState; save_state(SourceState()); print('state reset')"

echo "[2] start server (docker compose) in background"
docker compose up -d --build

sleep 2

echo "[3] POST sample event"
curl -s -X POST "http://127.0.0.1:8000/event" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"id":1,"timestamp":"2026-02-17T10:00:00Z","event_type":"WAN_LOSS","severity":"info","message":"wan down","device_id":"rutx50-01"}' \
  >/dev/null

echo "[4] verify chain (should be OK)"
python -m proofgraph.tools.verify --file proofgraph/output/proof.json

echo "[5] tamper proof (change message) + verify (should FAIL)"
python - <<'PY'
import json
p="proofgraph/output/proof.json"
data=json.load(open(p))
data[0]["canonical"]["message"]="tampered"
json.dump(data, open(p,"w"), indent=2)
print("tampered first entry")
PY

python -m proofgraph.tools.verify --file proofgraph/output/proof.json || true

echo "[6] shutdown"
docker compose down
