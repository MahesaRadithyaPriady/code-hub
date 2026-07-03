from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME
from app.database import Base, engine, ensure_database
from app.models.community import Community, user_communities  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.tech import Tech, user_techs  # noqa: F401
from app.models.user import User  # noqa: F401
from app.routes import auth as auth_router
from app.routes import community as community_router
from app.routes import role as role_router
from app.routes import tech as tech_router
from app.seeders.community import seed_communities
from app.seeders.role import seed_roles
from app.seeders.tech import seed_techs

app = FastAPI(title=APP_NAME)


@app.on_event("startup")
async def startup():
    await ensure_database()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_roles()
    await seed_techs()
    await seed_communities()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth_router.router)
app.include_router(role_router.router)
app.include_router(tech_router.router)
app.include_router(community_router.router)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
