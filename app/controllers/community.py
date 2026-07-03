from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community import Community
from app.schemas.community import CommunityCreate, CommunityUpdate


async def create_community(db: AsyncSession, data: CommunityCreate) -> Community:
    existing = await db.execute(
        select(Community).where(Community.nama_community == data.nama_community)
    )
    if existing.scalar():
        raise ValueError("Community name already exists")

    community = Community(
        nama_community=data.nama_community,
        color=data.color,
        description=data.description,
    )
    db.add(community)
    await db.commit()
    await db.refresh(community)
    return community


async def get_communities(db: AsyncSession) -> list[Community]:
    result = await db.execute(select(Community).order_by(Community.id))
    return result.scalars().all()


async def get_community_by_id(db: AsyncSession, community_id: int) -> Community | None:
    return await db.get(Community, community_id)


async def update_community(
    db: AsyncSession, community_id: int, data: CommunityUpdate
) -> Community | None:
    community = await db.get(Community, community_id)
    if not community:
        return None
    if data.nama_community is not None:
        community.nama_community = data.nama_community
    if data.color is not None:
        community.color = data.color
    if data.description is not None:
        community.description = data.description
    if data.is_active is not None:
        community.is_active = data.is_active
    await db.commit()
    await db.refresh(community)
    return community


async def delete_community(db: AsyncSession, community_id: int) -> bool:
    community = await db.get(Community, community_id)
    if not community:
        return False
    await db.delete(community)
    await db.commit()
    return True
