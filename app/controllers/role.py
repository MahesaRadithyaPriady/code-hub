from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


async def create_role(db: AsyncSession, data: RoleCreate) -> Role:
    existing = await db.execute(
        select(Role).where(Role.nama_role == data.nama_role)
    )
    if existing.scalar():
        raise ValueError("Role name already exists")

    role = Role(
        nama_role=data.nama_role,
        icon=data.icon,
        color=data.color,
        description=data.description,
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def get_roles(db: AsyncSession) -> list[Role]:
    result = await db.execute(select(Role).order_by(Role.id))
    return result.scalars().all()


async def get_role_by_id(db: AsyncSession, role_id: int) -> Role | None:
    return await db.get(Role, role_id)


async def update_role(
    db: AsyncSession, role_id: int, data: RoleUpdate
) -> Role | None:
    role = await db.get(Role, role_id)
    if not role:
        return None
    if data.nama_role is not None:
        role.nama_role = data.nama_role
    if data.icon is not None:
        role.icon = data.icon
    if data.color is not None:
        role.color = data.color
    if data.description is not None:
        role.description = data.description
    if data.is_active is not None:
        role.is_active = data.is_active
    await db.commit()
    await db.refresh(role)
    return role


async def delete_role(db: AsyncSession, role_id: int) -> bool:
    role = await db.get(Role, role_id)
    if not role:
        return False
    await db.delete(role)
    await db.commit()
    return True
