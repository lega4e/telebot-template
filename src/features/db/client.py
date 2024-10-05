import asyncio

from logging import Logger

from typing import Any, Dict

from sqlalchemy import insert, Result, update, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from lega4e_library.provider import Storage, provider

from src.domain.di import configProvider, loggerProvider
from src.features.db.di import sessionMakerProvider


@provider
class DbClient:

  def __init__(self, ref: Storage):
    self.ref = ref
    self.sessionMaker = self.ref(sessionMakerProvider)
    self.session: AsyncSession = self.sessionMaker()
    self.config = self.ref(configProvider)
    self.syslog: Logger = self.ref(loggerProvider)
    self._locked = False

  # SERVICE
  async def exec(self, stmt, commit: bool = True):
    return await self._exec(stmt, unpack=False, commit=commit)

  async def execu(self, stmt, commit: bool = True):
    return await self._exec(stmt, unpack=True, unpackOne=False, commit=commit)

  async def execo(self, stmt, commit: bool = True):
    return await self._exec(stmt, unpack=True, unpackOne=True, commit=commit)

  async def _exec(
    self,
    stmt,
    unpack: bool = True,
    unpackOne: bool = False,
    commit: bool = True,
  ):
    isFirst = True
    while True:
      try:
        await self._lock()
        result = await self.session.execute(stmt)
        if commit:
          await self.session.commit()
        await self.session.reset()
        self._unlock()
        return self._unpack(result, unpackOne) if unpack else result
      except Exception as e:
        self._unlock()
        self.syslog.error(e, exc_info=e)
        if not isFirst:
          raise Exception('Unhandled db error')
        isFirst = False
        self.session = self.sessionMaker()
        await asyncio.sleep(0.5)

  async def _lock(self):
    while self._locked:
      await asyncio.sleep(0.1)
    self._locked = True

  def _unlock(self):
    self._locked = False

  async def _updateOrInsert(
    self,
    table,
    where,
    values: Dict[str, Any],
    insertAdditionalValues: Dict[str, Any],
  ):
    stmt = update(table).where(where).values(**values)
    result: CursorResult = await self.exec(stmt)

    if result.rowcount == 0:
      stmt = insert(table).values(
        **values,
        **insertAdditionalValues,
      )
      await self.exec(stmt)

  @staticmethod
  def _unpack(result: Result, one: bool):
    result = [row[0] for row in result]
    if one:
      return None if len(result) == 0 else result[0]
    else:
      return result
