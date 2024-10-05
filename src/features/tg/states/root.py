from typing import Optional

from telebot.types import ReplyKeyboardMarkup, Message
from tgui.src.domain.piece import P
from tgui.src.states.tg_state import KeyboardAction

from src.features.tg.domain.emoji import emj
from src.features.tg.states.base import BaseState
from src.features.tg.domain.user_scope import UserScope


class RootState(BaseState):

  def getKeyboardMarkup(self) -> Optional[ReplyKeyboardMarkup]:
    return None
    # return self.buildKeyboard([btn.cancel])

  async def _handleCommandBefore(self, _: Message) -> bool:
    await self.u.init()
    return False

  async def _handleMessageBefore(self, _: Message) -> bool:
    await self.u.init()
    return False

  def __init__(self, u: UserScope):
    BaseState.__init__(self, u)

  async def _handleCommand(self, m: Message) -> bool:
    if m.text == '/start':
      await self.send(P('Hello'))
    else:
      await self.send(
        P('Неизвестная команда..', emoji=emj.fail),
        keyboardAction=KeyboardAction.reset(),
      )

    return True

  async def _handleMessage(self, m: Message) -> bool:
    await self.send(
      P('Не понимаю, что ты хочешь..', emoji=emj.fail),
      keyboardAction=KeyboardAction.reset(),
    )

    return True
