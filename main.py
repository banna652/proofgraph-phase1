import json
import os
import hashlib

from config import PROOF_FILE, HASH_ALGO
from sample_events import get_sample_events


def compute_hash(data: str) -> str:
    hash_func = hashlib.new(HASH_ALGO)
    hash_func.update(data.encode("utf-8"))
    return hash_func.hexdigest()

def load_existing_proofs() -> list:
    if not os.path.exists(PROOF_FILE):
        return []
    
    if os.path.getsize(PROOF_FILE) == 0:
        return []
    
    with open(PROOF_FILE, "r") as f:
        return json.load(f)
    
def save_proofs(proofs: list):
    with open(PROOF_FILE, "w") as f:
        json.dump(proofs, f, indent=2)
        
def get_last_hash(proofs: list) -> str:
    if not proofs:
        return "GENESIS"
    return proofs[-1]["hash"]
    
def generate_proofs():
    proofs = load_existing_proofs()
    previous_hash = get_last_hash(proofs)
    
    events = get_sample_events()
    
    for event in events:
        payload = json.dumps(event, sort_keys=True)
        
        combined_data = payload + previous_hash
        current_hash = compute_hash(combined_data)
        
        proof_entry = {
            "timestamp": event["timestamp"],
            "event_type": event["event_type"],
            "prev_hash": previous_hash,
            "hash": current_hash
        }
        
        proofs.append(proof_entry)
        previous_hash = current_hash
        
    save_proofs(proofs)
        
if __name__ == "__main__":
    generate_proofs()
    print("phase 1 proof generation completed.")
        