from dataclasses import asdict, dataclass
from typing import Optional

from config import STATE_FILE
from proofgraph.core.storage import load_json, save_json

@dataclass
class SourceState:
    last_id: int = 0 
    
def load_state() -> SourceState:
    data = load_json(STATE_FILE, default={"last_id": 0})
    
    try:
        last_id = int(data.get("last_id", 0))
    except Exception:
        last_id = 0
        
    return SourceState(last_id=last_id)

def save_state(state: SourceState) -> None:
    save_json(STATE_FILE, asdict(state))