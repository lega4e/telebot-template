from lega4e_library import Storage, provider
from tgui.src.domain.destination import TgDestination

from src.domain.di import loggerProvider
from src.features.db.client import DbClient


@provider
class UserScope:

  def __init__(self, ref: Storage, tgId: int):
    from src.features.tg.domain.di import tgProvider
    from src.features.tg.states.root import RootState

    self.ref = ref
    self.dst = TgDestination(chatId=tgId)
    self.tg = ref(tgProvider)
    self.db = ref(DbClient)
    self.log = ref(loggerProvider)
    self.root = RootState(self)
    self.initialized = False

  async def init(self):
    if self.initialized:
      return

    self.initialized = True
