# ProofGraph – Phase 2A (v1.1)

Deterministic Integrity Core (MVP)

ProofGraph Phase 2A implements a strictly deterministic, tamper-evident integrity engine.

This version is frozen under Phase 2A v1.1 scope and includes only the minimal deterministic integrity core.

---

## Scope (Phase 2A v1.1)

### Included

- Deterministic canonical normalization
- Sequential SHA-256 chaining
- Fixed genesis constant
- Append-only storage
- Persistent state tracking
- Same input → same hash guarantee
- Dockerized deployment
- Corruption detection test scenario

### Excluded (Out of Scope)

- No signature system
- No certificate endpoint
- No public verification mechanism
- No multi-device support
- No authentication hardening
- No scalability layer
- No production hardening

---

## Architecture Overview

Each incoming event is:

1. Canonically normalized (sorted, stable JSON)
2. Combined with previous hash
3. Hashed using SHA-256
4. Appended to an append-only proof file
5. State updated with `last_id` and `last_hash`

### Chain Formula

```
hash_n = SHA256( canonical_event + previous_hash )
```

### Genesis

```
previous_hash = "GENESIS_V1"
```

Any modification of stored data breaks the chain.

---

## API Endpoints

### POST /event

Ingests a canonical event and appends it to the integrity chain.

#### Required Headers

```
Authorization: Bearer <INGEST_TOKEN>
Content-Type: application/json
```

#### Example Payload

```json
{
  "id": 1,
  "timestamp": "2026-02-17T10:00:00Z",
  "event_type": "WAN_LOSS",
  "severity": "info",
  "message": "wan down",
  "device_id": "rutx50-01"
}
```

---

### GET /state

Returns current integrity state:

```json
{
  "last_id": 1,
  "last_hash": "<current_hash>"
}
```

---

## Project Structure

```
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
```

---

## Local Development (Docker)

### Build & Run

```
docker compose up --build
```

Server runs at:

```
http://localhost:8000
```

---

## Environment Variable

Set ingest token:

```
export INGEST_TOKEN=devtoken
```

---

## Manual Test

### Send Event

```
curl -X POST http://localhost:8000/event \
  -H "Authorization: Bearer devtoken" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"timestamp":"2026-02-17T10:00:00Z","event_type":"WAN_LOSS","severity":"info","message":"wan down","device_id":"rutx50-01"}'
```

### Check State

```
curl http://localhost:8000/state
```

---

## Verification Tool

Verify integrity:

```
python -m proofgraph.tools.verify --file proofgraph/output/proof.json
```

Replay entries:

```
python -m proofgraph.tools.verify --file proofgraph/output/proof.json --replay --limit 10
```

---

## Corruption Detection Test

Automated deterministic corruption test:

```
./tamper_test.sh
```

Expected result:

- First verification → OK
- After tampering → FAIL (hash mismatch detected)

---

## Determinism Guarantee

For identical canonical input:

- Same previous hash
- Same canonical normalization
- Same SHA-256 output
- Same resulting hash

ProofGraph Phase 2A guarantees strict determinism.

---

## Deployment

Phase 2A delivers:

- Self-contained Docker image
- docker-compose.yml
- Deterministic integrity core
- No VPS-specific configuration required

Deployment to VPS handled externally.

---

## Status

Phase 2A v1.1 — Implementation Complete  
Deterministic Core — Stable  
Scope — Frozen
