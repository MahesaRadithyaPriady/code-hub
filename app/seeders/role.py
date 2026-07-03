from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.role import Role

SEED_ROLES = [
    {
        "nama_role": "Frontend",
        "icon": "lucide:layout-dashboard",
        "color": "#3B82F6",
        "description": "Frontend developer - UI/UX, React, Flutter, dll",
    },
    {
        "nama_role": "Backend",
        "icon": "lucide:server",
        "color": "#10B981",
        "description": "Backend developer - API, database, server, dll",
    },
]


async def seed_roles():
    async with async_session() as db:
        for role_data in SEED_ROLES:
            existing = await db.execute(
                select(Role).where(Role.nama_role == role_data["nama_role"])
            )
            if not existing.scalar():
                role = Role(**role_data)
                db.add(role)
                print(f"[seeder] Role '{role_data['nama_role']}' created.")
            else:
                print(f"[seeder] Role '{role_data['nama_role']}' already exists.")
        await db.commit()
