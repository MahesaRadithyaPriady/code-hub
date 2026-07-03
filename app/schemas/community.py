from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommunityCreate(BaseModel):
    nama_community: str
    color: Optional[str] = None
    description: Optional[str] = None


class CommunityUpdate(BaseModel):
    nama_community: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CommunityOut(BaseModel):
    id: int
    nama_community: str
    color: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SelectCommunitiesRequest(BaseModel):
    community_ids: list[int]
