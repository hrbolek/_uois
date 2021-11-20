import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from functools import cache
from sqlengine import getBaseModel

@cache
async def init(connectionstring=None, doDropAll=False, doCreateAll=False):
    assert not(connectionstring is None), 'Connection string missing'

    engine = create_async_engine(connectionstring)

    BaseModel = getBaseModel()

    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    if doDropAll or doCreateAll:
        async with engine.begin() as conn:
            if doDropAll:
                await conn.run_sync(BaseModel.metadata.drop_all)
            if doCreateAll:
                await conn.run_sync(BaseModel.metadata.create_all)
        await engine.dispose()

    return Session

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with init()() as session: # two calls are perfect
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()