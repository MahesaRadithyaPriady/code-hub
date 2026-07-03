from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech import Tech
from app.schemas.tech import TechCreate, TechUpdate


async def create_tech(db: AsyncSession, data: TechCreate) -> Tech:
    existing = await db.execute(
        select(Tech).where(Tech.nama_tech == data.nama_tech)
    )
    if existing.scalar():
        raise ValueError("Tech name already exists")

    tech = Tech(
        nama_tech=data.nama_tech,
        color=data.color,
        description=data.description,
    )
    db.add(tech)
    await db.commit()
    await db.refresh(tech)
    return tech


async def get_techs(db: AsyncSession) -> list[Tech]:
    result = await db.execute(select(Tech).order_by(Tech.id))
    return result.scalars().all()


async def get_tech_by_id(db: AsyncSession, tech_id: int) -> Tech | None:
    return await db.get(Tech, tech_id)


async def update_tech(
    db: AsyncSession, tech_id: int, data: TechUpdate
) -> Tech | None:
    tech = await db.get(Tech, tech_id)
    if not tech:
        return None
    if data.nama_tech is not None:
        tech.nama_tech = data.nama_tech
    if data.color is not None:
        tech.color = data.color
    if data.description is not None:
        tech.description = data.description
    if data.is_active is not None:
        tech.is_active = data.is_active
    await db.commit()
    await db.refresh(tech)
    return tech


async def delete_tech(db: AsyncSession, tech_id: int) -> bool:
    tech = await db.get(Tech, tech_id)
    if not tech:
        return False
    await db.delete(tech)
    await db.commit()
    return True
