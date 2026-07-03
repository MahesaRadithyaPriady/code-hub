from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.controllers import tech as tech_controller
from app.database import get_db
from app.models.user import User
from app.schemas.tech import TechCreate, TechOut, TechUpdate

router = APIRouter(prefix="/techs", tags=["techs"])


@router.post("", response_model=TechOut, summary="Create tech")
async def create_tech(
    data: TechCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new tech (e.g. Python, React, Docker). Requires access token."""
    try:
        return await tech_controller.create_tech(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[TechOut], summary="List all techs")
async def list_techs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available techs. Requires access token."""
    return await tech_controller.get_techs(db)


@router.get("/{tech_id}", response_model=TechOut, summary="Get tech by ID")
async def get_tech(
    tech_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single tech by its ID. Requires access token."""
    tech = await tech_controller.get_tech_by_id(db, tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Tech not found")
    return tech


@router.put("/{tech_id}", response_model=TechOut, summary="Update tech")
async def update_tech(
    tech_id: int,
    data: TechUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing tech. Requires access token."""
    tech = await tech_controller.update_tech(db, tech_id, data)
    if not tech:
        raise HTTPException(status_code=404, detail="Tech not found")
    return tech


@router.delete("/{tech_id}", summary="Delete tech")
async def delete_tech(
    tech_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a tech by ID. Requires access token."""
    deleted = await tech_controller.delete_tech(db, tech_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tech not found")
    return {"detail": "Tech deleted"}
