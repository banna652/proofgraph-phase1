import json
from typing import Any, Dict, List

from config import HASH_ALGO
from proofgraph.core.hash import compute_hash

GENESIS = "GENESIS"

def last_hash(proofs: List[Dict[str, Any]]) -> str:
    return proofs[-1]["hash"] if proofs else GENESIS

def append_events(proofs: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prev = last_hash(proofs)
    
    for ev in events:
        # deterministic payload
        payload = json.dumps(ev, sort_keys=True, separators=(",", ":"))
        h = compute_hash(payload + prev, algo=HASH_ALGO)
        
        proofs.append({
            "event": ev,
            "prev_hash": prev,
            "hash": h
        })
        
        prev = h
        
    return proofs