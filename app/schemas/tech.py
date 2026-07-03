from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TechCreate(BaseModel):
    nama_tech: str
    color: Optional[str] = None
    description: Optional[str] = None


class TechUpdate(BaseModel):
    nama_tech: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TechOut(BaseModel):
    id: int
    nama_tech: str
    color: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SelectTechsRequest(BaseModel):
    tech_ids: list[int]
