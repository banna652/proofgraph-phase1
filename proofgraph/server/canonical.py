import json
from typing import Any, Dict

def canonicalize(event: Dict[str, Any]) -> str:
    return json.dumps(event, sort_keys=True, separators=(",", ":"))