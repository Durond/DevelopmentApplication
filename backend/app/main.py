import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/app")
if DATABASE_URL.startswith("postgresql+psycopg://"):
    ASYNC_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql+psycopg_async://", 1)
else:
    ASYNC_URL = DATABASE_URL

engine = create_async_engine(ASYNC_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await engine.dispose()


app = FastAPI(title="API", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-check")
async def db_check():
    async with SessionLocal() as session:
        result = await session.execute(text("SELECT 1 AS n"))
        row = result.mappings().first()
    return {"db": "ok", "result": int(row["n"]) if row else None}
