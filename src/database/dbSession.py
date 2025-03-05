from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI
from core.config import appSetting
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(appSetting.SQLALCHEMY_DATABASE_URI, echo=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with SessionLocal() as session:
        yield session


async def test_db_connection():
    try:
        async with engine.begin() as conn:
            # Ensure tables exist
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✅ Database connected successfully!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")


async def close_db():
    await engine.dispose()


async def lifespan(app: FastAPI):
    await test_db_connection()
    yield
    await close_db()


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
