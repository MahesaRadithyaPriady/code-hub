from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.controllers import role as role_controller
from app.database import get_db
from app.models.user import User
from app.schemas.role import RoleCreate, RoleOut, RoleUpdate

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("", response_model=RoleOut, summary="Create role")
async def create_role(
    data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new role (e.g. admin, member, moderator). Requires access token."""
    try:
        return await role_controller.create_role(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[RoleOut], summary="List all roles")
async def list_roles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available roles. Requires access token."""
    return await role_controller.get_roles(db)


@router.get("/{role_id}", response_model=RoleOut, summary="Get role by ID")
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single role by its ID. Requires access token."""
    role = await role_controller.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleOut, summary="Update role")
async def update_role(
    role_id: int,
    data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing role. Requires access token."""
    role = await role_controller.update_role(db, role_id, data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.delete("/{role_id}", summary="Delete role")
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a role by ID. Requires access token."""
    deleted = await role_controller.delete_role(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"detail": "Role deleted"}
