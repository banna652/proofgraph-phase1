from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Protocol

Event = Dict[str, object]

@dataclass
class SourceState:
    # Cursor state for incremental fetching.
    last_id: int = 0
    
class EventSource(Protocol):
    # All event sources (simulated, router, syslog) must implement fetch().
    name: str
    
    def fetch(self, state: SourceState) -> List[Event]:
        # Fetch new events (id > state.last_id) and return normalized canonical events.
        ...