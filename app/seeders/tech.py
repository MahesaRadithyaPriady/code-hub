from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.tech import Tech

SEED_TECHS = [
    {
        "nama_tech": "Python",
        "color": "#3776AB",
        "description": "General-purpose programming language",
    },
    {
        "nama_tech": "JavaScript",
        "color": "#F7DF1E",
        "description": "Web programming language",
    },
    {
        "nama_tech": "TypeScript",
        "color": "#3178C6",
        "description": "Typed superset of JavaScript",
    },
    {
        "nama_tech": "React",
        "color": "#61DAFB",
        "description": "Frontend UI library",
    },
    {
        "nama_tech": "Flutter",
        "color": "#02569B",
        "description": "Cross-platform mobile UI framework",
    },
    {
        "nama_tech": "PostgreSQL",
        "color": "#4169E1",
        "description": "Relational database management system",
    },
    {
        "nama_tech": "Docker",
        "color": "#2496ED",
        "description": "Containerization platform",
    },
    {
        "nama_tech": "FastAPI",
        "color": "#009688",
        "description": "Modern Python web framework",
    },
]


async def seed_techs():
    async with async_session() as db:
        for tech_data in SEED_TECHS:
            existing = await db.execute(
                select(Tech).where(Tech.nama_tech == tech_data["nama_tech"])
            )
            if not existing.scalar():
                tech = Tech(**tech_data)
                db.add(tech)
                print(f"[seeder] Tech '{tech_data['nama_tech']}' created.")
            else:
                print(f"[seeder] Tech '{tech_data['nama_tech']}' already exists.")
        await db.commit()
