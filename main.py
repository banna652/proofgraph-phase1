from __future__ import annotations
import argparse

from config import PROOF_FILE
from proofgraph.core.proof_generator import append_events
from proofgraph.core.storage import load_json, save_json
from proofgraph.core.state import load_state, save_state

from proofgraph.events.router import RutOSRouterSource
from proofgraph.events.simulated import get_events
from proofgraph.events.syslog import SyslogSource

def main() -> None:
    parser = argparse.ArgumentParser(description="ProofGraph V0 Phase 2 collector")
    parser.add_argument(
        "--source",
        choices=["simulated", "router", "syslog"],
        default="simulated",
        help="Event source to collect from"
    )
    args = parser.parse_args()
    
    proofs = load_json(PROOF_FILE, default=[])
    state = load_state()
    
    if args.source == "simulated":
        events = get_events()
        
    elif args.source == "router":
        src = RutOSRouterSource.from_env()
        events = src.fetch(state)
        
    else:
        src = SyslogSource()
        events = src.fetch(state)
        
    if not events:
        print("No new events.")
        return
    
    proofs = append_events(proofs, events)
    save_json(PROOF_FILE, proofs)
    
    max_id = max(int(e.get("id", 0)) for e in events)
    if max_id > int(state.last_id or 0):
        state.last_id = max_id
    save_state(state)
    
    print(f"Added {len(events)} events from source={args.source}")
    print(f"Proof file: {PROOF_FILE}")
    print(f"State file updated: last_id={state.last_id}")
    
if __name__ == "__main__":
    main()
