from urllib.parse import urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def _get_admin_url(url: str) -> str:
    parsed = urlparse(url)
    admin = parsed._replace(path="/postgres")
    return urlunparse(admin)


def _get_db_name(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path.lstrip("/")


async def ensure_database():
    db_name = _get_db_name(DATABASE_URL)
    admin_url = _get_admin_url(DATABASE_URL)
    admin_engine = create_async_engine(
        admin_url, echo=False, isolation_level="AUTOCOMMIT"
    )
    try:
        async with admin_engine.connect() as conn:
            result = await conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": db_name},
            )
            if not result.scalar():
                await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"[startup] Database '{db_name}' created.")
            else:
                print(f"[startup] Database '{db_name}' already exists.")
    finally:
        await admin_engine.dispose()


async def get_db():
    async with async_session() as session:
        yield session
