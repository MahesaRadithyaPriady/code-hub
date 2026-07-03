from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.controllers import auth as auth_controller
from app.database import get_db
from app.models.user import User
from app.schemas.community import CommunityOut, SelectCommunitiesRequest
from app.schemas.tech import SelectTechsRequest, TechOut
from app.schemas.user import (
    GoogleLoginRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    SelectRoleRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, summary="Register new user")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user with username/password. Returns access token and refresh token."""
    try:
        return await auth_controller.register(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse, summary="Login user")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login with username and password. Returns access token and refresh token."""
    try:
        return await auth_controller.login(db, data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=TokenResponse, summary="Refresh access token")
async def refresh(data: RefreshRequest):
    """Exchange a valid refresh token for a new access token and refresh token."""
    try:
        return await auth_controller.refresh_token(data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/google", response_model=TokenResponse, summary="Login with Google OAuth")
async def google_login(data: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    """Login or register via Google OAuth authorization code. Returns access token and refresh token."""
    try:
        return await auth_controller.google_login(db, data.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserOut, summary="Get current user")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get the authenticated user's profile including photo, bio, and address."""
    return current_user


@router.put("/me", response_model=UserOut, summary="Update current user profile")
async def update_profile(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the authenticated user's profile (name, photo_profile, bio, address). Only provided fields will be updated."""
    try:
        return await auth_controller.update_profile(db, current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/role", summary="Check if current user has a role")
async def check_role(current_user: User = Depends(get_current_user)):
    """Check whether the authenticated user has selected a role or not."""
    if current_user.role_id:
        return {"has_role": True, "role_id": current_user.role_id}
    return {"has_role": False, "role_id": None}


@router.put("/role", response_model=UserOut, summary="Select role for current user")
async def select_role(
    data: SelectRoleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Select a role for the authenticated user. User can only have one role."""
    try:
        return await auth_controller.select_role(db, current_user.id, data.role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/techs", response_model=list[TechOut], summary="Get current user techs")
async def get_my_techs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all techs selected by the authenticated user. Requires access token."""
    try:
        return await auth_controller.get_user_techs(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/techs/check", summary="Check if current user has techs")
async def check_techs(current_user: User = Depends(get_current_user)):
    """Check whether the authenticated user has selected any techs or not."""
    has_techs = len(current_user.techs) > 0 if current_user.techs else False
    return {
        "has_techs": has_techs,
        "tech_ids": [t.id for t in current_user.techs] if has_techs else [],
    }


@router.put("/techs", response_model=UserOut, summary="Select techs for current user")
async def select_techs(
    data: SelectTechsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Select one or more techs for the authenticated user. Replaces previous selection."""
    try:
        return await auth_controller.select_techs(db, current_user.id, data.tech_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/communities", response_model=list[CommunityOut], summary="Get current user communities")
async def get_my_communities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all communities selected by the authenticated user. Requires access token."""
    try:
        return await auth_controller.get_user_communities(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/communities/check", summary="Check if current user has communities")
async def check_communities(current_user: User = Depends(get_current_user)):
    """Check whether the authenticated user has selected any communities or not."""
    has_communities = len(current_user.communities) > 0 if current_user.communities else False
    return {
        "has_communities": has_communities,
        "community_ids": [c.id for c in current_user.communities] if has_communities else [],
    }


@router.put("/communities", response_model=UserOut, summary="Select communities for current user")
async def select_communities(
    data: SelectCommunitiesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Select one or more communities for the authenticated user. Replaces previous selection."""
    try:
        return await auth_controller.select_communities(db, current_user.id, data.community_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
