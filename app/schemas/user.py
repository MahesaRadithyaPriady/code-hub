from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.community import CommunityOut
from app.schemas.role import RoleOut
from app.schemas.tech import TechOut


class UserCreate(BaseModel):
    name: str
    username: str
    email: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: str
    photo_profile: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    provider: str
    role: Optional[RoleOut] = None
    techs: list[TechOut] = []
    communities: list[CommunityOut] = []
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Auth Schemas
# ---------------------------------------------------------------------------
class RegisterRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str


class SelectRoleRequest(BaseModel):
    role_id: int


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class GoogleLoginRequest(BaseModel):
    code: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    photo_profile: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None

