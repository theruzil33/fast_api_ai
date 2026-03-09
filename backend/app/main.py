from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.core.exception_handlers import register_exception_handlers
from app.core.security import hash_password
import app.models  # noqa: F401 — register all models


async def _create_initial_user() -> None:
    if not settings.INITIAL_USER_USERNAME or not settings.INITIAL_USER_PASSWORD:
        return

    from app.models.user import User

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == settings.INITIAL_USER_USERNAME))
        if result.scalar_one_or_none() is None:
            db.add(User(
                username=settings.INITIAL_USER_USERNAME,
                hashed_password=hash_password(settings.INITIAL_USER_PASSWORD),
            ))
            await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await _create_initial_user()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")
