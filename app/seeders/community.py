from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.community import Community

SEED_COMMUNITIES = [
    {
        "nama_community": "Web Development",
        "color": "#3B82F6",
        "description": "Komunitas untuk web developer - frontend, backend, fullstack",
    },
    {
        "nama_community": "Mobile Development",
        "color": "#10B981",
        "description": "Komunitas untuk mobile developer - Android, iOS, Flutter",
    },
    {
        "nama_community": "Data Science",
        "color": "#8B5CF6",
        "description": "Komunitas untuk data scientist dan analyst",
    },
    {
        "nama_community": "DevOps",
        "color": "#F59E0B",
        "description": "Komunitas untuk DevOps engineer - CI/CD, cloud, infrastructure",
    },
    {
        "nama_community": "UI/UX Design",
        "color": "#EC4899",
        "description": "Komunitas untuk designer - UI, UX, product design",
    },
    {
        "nama_community": "Game Development",
        "color": "#EF4444",
        "description": "Komunitas untuk game developer - Unity, Unreal, Godot",
    },
]


async def seed_communities():
    async with async_session() as db:
        for community_data in SEED_COMMUNITIES:
            existing = await db.execute(
                select(Community).where(
                    Community.nama_community == community_data["nama_community"]
                )
            )
            if not existing.scalar():
                community = Community(**community_data)
                db.add(community)
                print(f"[seeder] Community '{community_data['nama_community']}' created.")
            else:
                print(f"[seeder] Community '{community_data['nama_community']}' already exists.")
        await db.commit()
