from __future__ import annotations
import socket
from datetime import datetime, timezone
from typing import List

from proofgraph.core.state import SourceState
from proofgraph.events.base import Event

class SyslogSource:
    name = "syslog"
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5140, max_lines: int = 100) -> None:
        self.host = host
        self.port = port
        self.max_lines = max_lines
        
    def fetch(self, state: SourceState) -> List[Event]:
        events: List[Event] = []
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        sock.settimeout(2.0)
        
        seq = int(state.last_id or 0)
        
        try:
            while len(events) < self.max_lines:
                data, _ = sock.recvfrom(8192)
                line = data.decode("utf-8", errors="replace").strip()
                seq += 1
                
                events.append({
                    "id": seq,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event_type": "SYSLOG",
                    "severity": None,
                    "facility": None,
                    "message": line,
                    "source": self.name,
                })
        except socket.timeout:
            pass
        finally:
            sock.close()
            
        return events