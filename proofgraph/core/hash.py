import hashlib

def compute_hash(data: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    h.update(data.encode("utf-8"))
    return h.hexdigest()