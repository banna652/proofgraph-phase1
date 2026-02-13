from pathlib import Path

HASH_ALGO = "sha256"

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "proofgraph" / "output"
PROOF_FILE = OUTPUT_DIR / "proof.json"
STATE_FILE = OUTPUT_DIR / "state.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)