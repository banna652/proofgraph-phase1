from __future__ import annotations
from typing import Dict, List, Protocol

from proofgraph.core.state import SourceState

Event = Dict[str, object]
    
class EventSource(Protocol):
    # All event sources (simulated, router, syslog) must implement fetch().
    name: str
    
    def fetch(self, state: SourceState) -> List[Event]:
        # Fetch new events (id > state.last_id) and return normalized canonical events.
        ...