from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RoleCreate(BaseModel):
    nama_role: str
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    nama_role: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleOut(BaseModel):
    id: int
    nama_role: str
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
