import argparse
import json
from pathlib import Path

from config import HASH_ALGO
from proofgraph.core.hash import compute_hash

GENESIS_OK = {"GENESIS", "0"}

def load(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def verify(proofs):
    if not proofs:
        print("OK: proof file empty (0 entries).")
        return True

    prev_hash_expected = None

    for i, p in enumerate(proofs):
        ev = {"timestamp": p["timestamp"], "event_type": p["event_type"]}
        prev_hash = p["prev_hash"]
        stored = p["hash"]

        if i == 0:
            if prev_hash not in GENESIS_OK:
                print(f"FAIL @ {i}: first prev_hash should be GENESIS/0, got {prev_hash}")
                return False
        else:
            if prev_hash != prev_hash_expected:
                print(f"FAIL @ {i}: chain broken (prev_hash mismatch)")
                return False

        payload = json.dumps(ev, sort_keys=True)
        computed = compute_hash(payload + prev_hash, algo=HASH_ALGO)

        if computed != stored:
            print(f"FAIL @ {i}: hash mismatch (tampering detected)")
            return False

        prev_hash_expected = stored

    print(f"OK: chain valid ({len(proofs)} entries)")
    return True

def replay(proofs, limit=0):
    n = len(proofs) if limit <= 0 else min(limit, len(proofs))
    for i in range(n):
        p = proofs[i]
        print(f"[{i}] {p['timestamp']} | {p['event_type']} | prev={p['prev_hash'][:10]}.. | hash={p['hash'][:10]}..")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="proofgraph/output/proof.json")
    ap.add_argument("--replay", action="store_true")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    proofs = load(Path(args.file))
    ok = verify(proofs)

    if ok and args.replay:
        replay(proofs, args.limit)

    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()