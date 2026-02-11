from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.config.settings import get_settings

_settings = get_settings()

async_engine: AsyncEngine = create_async_engine(
    _settings.POSTGRES_DSN,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
