from datetime import datetime, timezone
from typing import Dict, List

def get_events() -> List[Dict]:
    def ts():
        return datetime.now(timezone.utc).isoformat()

    return [
        {"timestamp": ts(), "event_type": "WAN_LOSS"},
        {"timestamp": ts(), "event_type": "FAILOVER_TRIGGERED"},
        {"timestamp": ts(), "event_type": "WAN_RECOVERY"},
    ]