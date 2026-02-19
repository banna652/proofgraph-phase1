# ProofGraph – Phase 2A (v1.1)

ProofGraph Phase 2A implements a strictly deterministic, tamper-evident integrity engine.

This implementation follows the frozen Phase 2A v1.1 scope. No features beyond this specification are included.

---------------------------------------------------------------------

SCOPE (Phase 2A v1.1)

Included:
- Deterministic canonical normalization
- Sequential SHA-256 chaining
- Fixed genesis constant
- Append-only storage
- Persistent state tracking
- Same input → same hash guarantee
- Dockerized deployment
- Corruption detection test scenario

Excluded (Out of Scope):
- No signature system
- No certificate endpoint
- No public verification mechanism
- No multi-device support
- No authentication hardening
- No scalability layer
- No production hardening

---------------------------------------------------------------------

ARCHITECTURE OVERVIEW

Each incoming event is:
1) Canonically normalized (sorted, stable JSON)
2) Combined with the previous hash
3) Hashed using SHA-256
4) Appended to an append-only proof file
5) State updated with last_id and last_hash

Chain formula:
hash_n = SHA256(canonical_event + previous_hash)

Genesis constant:
previous_hash = "GENESIS_V1"

Any modification, deletion, or reordering of stored entries breaks the chain.

---------------------------------------------------------------------

API ENDPOINTS

POST /event

Headers:
Authorization: Bearer <INGEST_TOKEN>
Content-Type: application/json

Example payload:
{
  "id": 1,
  "timestamp": "2026-02-17T10:00:00Z",
  "event_type": "WAN_LOSS",
  "severity": "info",
  "message": "wan down",
  "device_id": "rutx50-01"
}

GET /state

Returns:
{
  "last_id": 1,
  "last_hash": "<current_hash>"
}

---------------------------------------------------------------------

PROJECT STRUCTURE

proofgraph_v0/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── tamper_test.sh
├── README.md
└── proofgraph/
    ├── config.py
    ├── core/
    │   ├── hash.py
    │   ├── state.py
    │   ├── storage.py
    │   └── proof_generator.py
    ├── server/
    │   ├── app.py
    │   ├── auth.py
    │   ├── canonical.py
    │   └── schema.py
    ├── tools/
    │   └── verify.py
    └── output/
        ├── proof.json
        └── state.json

---------------------------------------------------------------------

LOCAL DEVELOPMENT (Docker)

Build and run:
docker compose up --build

Server runs at:
http://localhost:8000

---------------------------------------------------------------------

ENVIRONMENT VARIABLE

Set ingest token before sending events:
export INGEST_TOKEN=devtoken

Note:
INGEST_TOKEN must match the Authorization header for POST /event.

---------------------------------------------------------------------

MANUAL TEST

Send event:
curl -X POST http://localhost:8000/event \
  -H "Authorization: Bearer devtoken" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"timestamp":"2026-02-17T10:00:00Z","event_type":"WAN_LOSS","severity":"info","message":"wan down","device_id":"rutx50-01"}'

Check state:
curl http://localhost:8000/state

---------------------------------------------------------------------

VERIFICATION TOOL

Verify integrity:
python -m proofgraph.tools.verify --file proofgraph/output/proof.json

Replay entries:
python -m proofgraph.tools.verify --file proofgraph/output/proof.json --replay --limit 10

---------------------------------------------------------------------

CORRUPTION DETECTION TEST

Run deterministic tamper test:
./tamper_test.sh

Expected:
First verification → OK
After tampering → FAIL (hash mismatch detected)

---------------------------------------------------------------------

DETERMINISM GUARANTEE

For identical canonical input:
- Same previous hash
- Same canonical normalization
- Same SHA-256 output
- Same resulting hash

ProofGraph Phase 2A guarantees strict determinism.

---------------------------------------------------------------------

DEPLOYMENT

Phase 2A delivers:
- Self-contained Docker image
- docker-compose configuration
- Deterministic integrity core
- No VPS-specific configuration required

Deployment to VPS handled externally.

---------------------------------------------------------------------

STATUS

Phase 2A v1.1 — Implementation Complete
Deterministic Core — Stable
Scope — Frozen
