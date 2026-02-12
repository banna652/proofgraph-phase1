from config import PROOF_FILE
from proofgraph.core.storage import load_json, save_json
from proofgraph.core.proof_generator import append_events
from proofgraph.events.simulated import get_events

def main():
    proofs = load_json(PROOF_FILE, default=[])
    events = get_events()

    proofs = append_events(proofs, events)
    save_json(PROOF_FILE, proofs)

    print(f"Done. Proof entries: {len(proofs)}")
    print(f"File: {PROOF_FILE}")

if __name__ == "__main__":
    main()
