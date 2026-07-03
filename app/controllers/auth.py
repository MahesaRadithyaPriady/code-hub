from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.google import get_google_userinfo
from app.auth.jwt import create_access_token, create_refresh_token, verify_token
from app.auth.password import hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest, UpdateProfileRequest


async def register(db: AsyncSession, data: RegisterRequest) -> dict:
    existing = await db.execute(
        select(User).where(
            (User.username == data.username) | (User.email == data.email)
        )
    )
    if existing.scalar():
        raise ValueError("Username or email already registered")

    user = User(
        name=data.name,
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        provider="local",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token_data = {"sub": str(user.id), "username": user.username}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }


async def select_role(db: AsyncSession, user_id: int, role_id: int) -> User:
    from app.models.role import Role

    role = await db.get(Role, role_id)
    if not role:
        raise ValueError("Role not found")

    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    user.role_id = role_id
    await db.commit()
    await db.refresh(user)
    return user


async def select_techs(db: AsyncSession, user_id: int, tech_ids: list[int]) -> User:
    from app.models.tech import Tech

    techs = []
    for tid in tech_ids:
        tech = await db.get(Tech, tid)
        if not tech:
            raise ValueError(f"Tech with id {tid} not found")
        techs.append(tech)

    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    user.techs = techs
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_techs(db: AsyncSession, user_id: int) -> list:
    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    return user.techs


async def select_communities(
    db: AsyncSession, user_id: int, community_ids: list[int]
) -> User:
    from app.models.community import Community

    communities = []
    for cid in community_ids:
        community = await db.get(Community, cid)
        if not community:
            raise ValueError(f"Community with id {cid} not found")
        communities.append(community)

    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    user.communities = communities
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_communities(db: AsyncSession, user_id: int) -> list:
    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    return user.communities


async def update_profile(
    db: AsyncSession, user_id: int, data: UpdateProfileRequest
) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    if data.name is not None:
        user.name = data.name
    if data.photo_profile is not None:
        from app.utils.image import save_base64_image
        user.photo_profile = save_base64_image(data.photo_profile)
    if data.bio is not None:
        user.bio = data.bio
    if data.address is not None:
        user.address = data.address

    await db.commit()
    await db.refresh(user)
    return user


async def login(db: AsyncSession, data: LoginRequest) -> dict:
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar()
    if not user or not user.password_hash:
        raise ValueError("Invalid username or password")
    if not verify_password(data.password, user.password_hash):
        raise ValueError("Invalid username or password")

    token_data = {"sub": str(user.id), "username": user.username}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }


async def refresh_token(token: str) -> dict:
    payload = verify_token(token)
    if not payload or payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")

    token_data = {"sub": payload["sub"], "username": payload.get("username", "")}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }


async def google_login(db: AsyncSession, code: str) -> dict:
    userinfo = await get_google_userinfo(code)
    if not userinfo:
        raise ValueError("Failed to get Google user info")

    email = userinfo.get("email")
    google_id = userinfo.get("sub")
    name = userinfo.get("name", email)

    if not email:
        raise ValueError("Google account has no email")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar()

    if not user:
        username = email.split("@")[0]
        user = User(
            name=name,
            username=username,
            email=email,
            provider="google",
            provider_id=google_id,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token_data = {"sub": str(user.id), "username": user.username}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }
