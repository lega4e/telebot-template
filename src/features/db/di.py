from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.domain.di import configProvider
from lega4e_library.provider import provider, Storage

from src.domain.models.config import DbConfig


@provider
def databaseEngineProvider(ref: Storage):
  db: DbConfig = ref(configProvider).db

  return create_async_engine(
    f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}',
    echo=False,
    poolclass=NullPool,
  )


@provider
def sessionMakerProvider(ref: Storage):
  engine = ref(databaseEngineProvider)
  return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
