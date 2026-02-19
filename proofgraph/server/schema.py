from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class EventSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: int = Field(..., ge=0)
    timestamp: datetime
    event_type: str
    severity: str
    message: str
    device_id: str