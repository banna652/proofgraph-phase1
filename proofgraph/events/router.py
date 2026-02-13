from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
import requests

from proofgraph.core.state import SourceState
from proofgraph.events.base import Event

class RutOSRouterSource:
    name = "rutos_api"
    
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        verify_tls: bool = False,
        timeout_s: int = 10,
        page_limit: int = 50,
        login_path: str = "/events_log",
        events_path: str = "/events_log",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_tls = verify_tls
        self.timeout_s = timeout_s
        self.page_limit = page_limit
        self.login_path = login_path
        self.events_path = events_path
        self.session = requests.Session()
        
    @classmethod
    def from_env(cls) -> "RutOSRouterSource":
        def must(name: str) -> str:
            v = os.getenv(name)
            if not v:
                raise RuntimeError(f"Missing env var: {name}")
            return v
        
        return cls(
            base_url=must("RUTOS_BASE_URL"),
            username=must("RUTOS_USERNAME"),
            password=must("RUTOS_PASSWORD"),
            verify_tls=os.getenv("RUTOS_VERIFY_TLS", "0") == "1",
            timeout_s=int(os.getenv("RUTOS_TIMEOUT_S", "10")),
            page_limit=int(os.getenv("RUTOS_PAGE_LIMIT", "50")),
            login_path=os.getenv("RUTOS_LOGIN_PATH", "/api/login"),
            events_path=os.getenv("RUTOS_EVENTS_PATH", "/events_log"),
        )
        
    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"
    
    def login(self) -> None:
        url = self._url(self.login_path)
        payload = {"username": self.username, "password": self.password}
        
        r = self.session.post(
            url, json=payload, timeout=self.timeout_s, verify=self.verify_tls
        )
        r.raise_for_status()
        
        try:
            data = r.json()
            if isinstance(data, dict) and data.get("success") is False:
                raise RuntimeError(f"RutOS login failed: {data}")
        except ValueError:
            pass
    
    def fetch_page(self, limit: int, offset: int) -> Dict[str, Any]:
        url = self._url(self.events_path)
        params = {"limit": limit, "offset": offset}
        r = self.session.get(
            url, params=params, timeout=self.timeout_s, verify=self.verify_tls
        )
        r.raise_for_status()
        return r.json()
    
    def normalize(self, raw: Dict[str, Any]) -> Event:
        raw_id = raw.get("id")
        try:
            eid = int(raw_id)
        except Exception:
            eid = 0
            
        timestamp = raw.get("time") or raw.get("date") or ""
        
        severity = raw.get("severity") or raw.get("type")
        
        facility = raw.get("facility")
        ev_type = raw.get("event_type") or facility or "UNKNOWN"
        
        message = raw.get("message") or raw.get("event") or ""
        
        return {
            "id": eid,
            "timestamp": str(timestamp),
            "event_type": str(ev_type),
            "severity": str(severity) if severity is not None else None,
            "facility": str(facility) if facility is not None else None,
            "message": str(message),
            "source": self.name,
        }
        
    def fetch(self, state: SourceState) -> List[Event]:
        self.login()
        
        last_id = int(state.last_id or 0)
        events: List[Event] = []
        
        offset = 0
        limit = self.page_limit
        total: Optional[int] = None
        
        while total is None or offset < total:
            payload = self.fetch_page(limit=limit, offset=offset)
            
            if isinstance(payload, dict) and "data" in payload:
                data_list = payload.get("data") or []
                pag = payload.get("pagination") or {}
                total = int(pag.get("total", total or 0))
                
                for raw in data_list:
                    ev = self.normalize(raw)
                    if int(ev["id"]) > last_id:
                        events.append(ev)
                        
            else:
                if isinstance(payload, dict) and "id" in payload:
                    ev = self.normalize(payload)
                    if int(ev["id"]) > last_id:
                        events.append(ev)
                total = 0
                
            offset += limit
            if total == 0:
                 break
            
        events.sort(key=lambda e: int(e.get("id", 0)))
        return events