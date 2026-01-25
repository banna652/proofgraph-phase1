from datetime import datetime


def get_sample_events():
    return [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "WAN_LOSS"
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "FAILOVER_TRIGGERED"
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "RECOVERY"
        }
    ]