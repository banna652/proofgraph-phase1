import json
from datetime import timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List

from fastapi import Depends, FastAPI
from pydantic import ValidationError

from proofgraph.config import PROOF_FILE
from proofgraph.core.state import GENESIS, SourceState, load_state, save_state
from proofgraph.server.auth import verify_token
from proofgraph.server.schema import EventSchema
from proofgraph.server.canonical import canonicalize

app = FastAPI(title="ProofGraph Phase 2A", version="1.1")

def _load_proof() -> List[Dict[str, Any]]:
    if not PROOF_FILE.exists():
        return []
    try:
        return json.loads(PROOF_FILE.read_text())
    except Exception:
        return []
    
def _append_proof(entry: Dict[str, Any]) -> None:
    PROOF_FILE.parent.mkdir(parents=True, exist_ok=True)
    proof = _load_proof()
    proof.append(entry)
    PROOF_FILE.write_text(json.dumps(proof, indent=2))
    
def _hash(payload: str) -> str:
    return sha256(payload.encode("utf-8")).hexdigest()

@app.post("/event")
def ingest_event(payload: Dict[str, Any], _=Depends(verify_token)):
    try:
        ev = EventSchema(**payload)
    except ValidationError as e:
        return {"ok": False, "error": e.errors()}
    
    ts_utc = ev.timestamp.astimezone(timezone.utc).replace(microsecond=0)
    canonical_event = {
        "id": ev.id,
        "timestamp": ts_utc.isoformat().replace("+00:00", "Z"),
        "event_type": ev.event_type.strip(),
        "severity": ev.severity.strip(),
        "message": ev.message.strip(),
        "device_id": ev.device_id.strip(),
    }
    
    canonical_json = canonicalize(canonical_event)
    
    st = load_state()
    prev_hash = st.last_hash or GENESIS
    
    new_hash = _hash(canonical_json + prev_hash)
    
    proof_entry = {
        "canonical": canonical_event,
        "prev_hash": prev_hash,
        "hash": new_hash,
    }
    _append_proof(proof_entry)
    
    st.last_id = max(st.last_id, ev.id)
    st.last_hash = new_hash
    save_state(st)
    
    return {"ok": True, "prev_hash": prev_hash, "hash": new_hash}

@app.get("/state")
def get_state():
    st = load_state()
    proofs = _load_proof()
    return {
        "last_id": st.last_id,
        "last_hash": st.last_hash,
        "proof_count": len(proofs),
    }