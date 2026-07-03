from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.controllers import community as community_controller
from app.database import get_db
from app.models.user import User
from app.schemas.community import CommunityCreate, CommunityOut, CommunityUpdate

router = APIRouter(prefix="/communities", tags=["communities"])


@router.post("", response_model=CommunityOut, summary="Create community")
async def create_community(
    data: CommunityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new community. Requires access token."""
    try:
        return await community_controller.create_community(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[CommunityOut], summary="List all communities")
async def list_communities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available communities. Requires access token."""
    return await community_controller.get_communities(db)


@router.get("/{community_id}", response_model=CommunityOut, summary="Get community by ID")
async def get_community(
    community_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single community by its ID. Requires access token."""
    community = await community_controller.get_community_by_id(db, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community


@router.put("/{community_id}", response_model=CommunityOut, summary="Update community")
async def update_community(
    community_id: int,
    data: CommunityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing community. Requires access token."""
    community = await community_controller.update_community(db, community_id, data)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community


@router.delete("/{community_id}", summary="Delete community")
async def delete_community(
    community_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a community by ID. Requires access token."""
    deleted = await community_controller.delete_community(db, community_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Community not found")
    return {"detail": "Community deleted"}
