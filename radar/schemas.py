from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Alert(BaseModel):
    id: str
    source: str = "nws"
    event_type: str  # e.g., "Severe Thunderstorm Warning"
    severity: Optional[str] = None  # e.g., "Severe", "Moderate"
    headline: Optional[str] = None
    description: Optional[str] = None
    instruction: Optional[str] = None
    onset: Optional[datetime] = None
    expires: Optional[datetime] = None
    sent: Optional[datetime] = None
    updated: Optional[datetime] = None
    area: Optional[str] = None  # free text area description
    counties: List[str] = Field(default_factory=list)
    latitude: Optional[float] = None  # centroid if available
    longitude: Optional[float] = None
    raw_url: Optional[str] = None  # link to the full alert
