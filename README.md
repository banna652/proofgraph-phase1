# ProofGraph V0 – Phase 1

## Purpose
Phase 1 demonstrates a minimal proof-generation flow using simulated network events.
It creates a deterministic, append-only hash chain that can later be integrated with real router logs in Phase 2.

---

## What Phase 1 Does
- Uses simulated network events (WAN loss, failover, recovery)
- Generates a SHA-256 hash chain for each event
- Stores proofs in a single append-only JSON file
- Ensures each event is cryptographically linked to the previous one

---

## What Phase 1 Does NOT Do
- No real router integration
- No SSH access to the router
- No real log parsing
- No verification script (will be added in Phase 2)

---

## Project Structure