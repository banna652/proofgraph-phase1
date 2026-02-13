from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict, Any


def get_events() -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()

    return [
        {
            "id": 1,
            "timestamp": now,
            "event_type": "WAN_LOSS",
            "severity": "warning",
            "facility": "network",
            "message": "Simulated WAN down",
            "source": "simulated",
        },
        {
            "id": 2,
            "timestamp": now,
            "event_type": "FAILOVER_TRIGGERED",
            "severity": "info",
            "facility": "network",
            "message": "Simulated failover triggered",
            "source": "simulated",
        },
        {
            "id": 3,
            "timestamp": now,
            "event_type": "WAN_RECOVERY",
            "severity": "info",
            "facility": "network",
            "message": "Simulated WAN recovered",
            "source": "simulated",
        },
    ]