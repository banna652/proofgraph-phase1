from dataclasses import asdict, dataclass

from proofgraph.config import STATE_FILE
from proofgraph.core.storage import load_json, save_json

GENESIS = "GENESIS_V1"

@dataclass
class SourceState:
    last_id: int = 0
    last_hash: str = GENESIS


def load_state() -> SourceState:
    data = load_json(
        STATE_FILE,
        default={"last_id": 0, "last_hash": GENESIS}
    )

    try:
        last_id = int(data.get("last_id", 0))
    except Exception:
        last_id = 0

    last_hash = data.get("last_hash", GENESIS)

    return SourceState(last_id=last_id, last_hash=last_hash)


def save_state(state: SourceState) -> None:
    save_json(STATE_FILE, asdict(state))