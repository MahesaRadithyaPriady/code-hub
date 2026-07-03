from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    user = User(name=data.name, username=data.username, email=data.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.id))
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def update_user(db: AsyncSession, user_id: int, data: UserUpdate) -> User | None:
    user = await db.get(User, user_id)
    if not user:
        return None
    if data.name is not None:
        user.name = data.name
    if data.username is not None:
        user.username = data.username
    if data.email is not None:
        user.email = data.email
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await db.get(User, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
