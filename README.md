# ProofGraph V0

Tamper-evident, append-only network continuity proof system.

---

# Phase 1 (Completed)

## Purpose
Phase 1 demonstrates a minimal proof-generation flow using simulated network events.

It builds a deterministic SHA-256 hash chain and validates integrity locally.

## Phase 1 Capabilities
- Simulated WAN loss / failover / recovery events
- SHA-256 hash chaining
- Append-only proof file (`proof.json`)
- Verification tool with replay support
- Tamper detection (hash mismatch detection)

---

# Phase 2 (In Progress – Edge-Centric Architecture)

Phase 2 integrates ProofGraph with a real Teltonika RUTX50 router.

Architecture direction (confirmed by Teltonika engineering):

- No RMS webhooks
- RMS logs are RMS-initiated only
- Router-level events must be collected from:
  - RutOS Web API (Events Log endpoint)
  - or Syslog forwarding

## Phase 2 Goals

- Collect structured router events at the edge
- Normalize events into canonical format
- Generate append-only SHA-256 hash chain
- Persist cursor state (`state.json`) for incremental ingestion
- Provide verification + replay tooling
- No UI / No cloud (edge-focused validation)

---

# Project Structure

proofgraph_v0/
├── config.py
├── main.py
├── requirements.txt
├── .env.example
└── proofgraph/
    ├── core/
    │   ├── hash.py
    │   ├── proof_generator.py
    │   ├── state.py
    │   └── storage.py
    ├── events/
    │   ├── base.py
    │   ├── simulated.py
    │   ├── router.py
    │   └── syslog.py
    └── tools/
        └── verify.py

---

# How to Run

## Install
pip install -r requirements.txt

---

## Simulated Mode

python3 main.py --source simulated
python3 -m proofgraph.tools.verify --file proofgraph/output/proof.json --replay --limit 10

---

## Router Mode (RutOS API over WireGuard)

Set environment variables:

export RUTOS_BASE_URL="https://<router_tunnel_ip>"
export RUTOS_USERNAME="..."
export RUTOS_PASSWORD="..."
export RUTOS_VERIFY_TLS=0

Then run:

python3 main.py --source router
python3 -m proofgraph.tools.verify --file proofgraph/output/proof.json --replay --limit 10

---

## Reset Output

rm -f proofgraph/output/proof.json proofgraph/output/state.json
python3 -c "from proofgraph.core.state import save_state, SourceState; save_state(SourceState(last_id=0)); print('state reset')"

---

# Security Notes

- Proof entries store full normalized event payload
- Each event is hash-linked to the previous one
- Any modification breaks the chain
- Cursor state ensures incremental ingestion (id > last_id)

---

# Status

Phase 1: Complete  
Phase 2: In progress (awaiting WireGuard endpoint parameters)