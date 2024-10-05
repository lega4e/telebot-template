import asyncio
import locale

from logging import Logger

from lega4e_library import storage
from telebot.async_telebot import AsyncTeleBot
from tgui.src.managers.tg_state_binder import TgStateBinder

from src.domain.di import configProvider, loggerProvider
from src.domain.models.config import Config
from src.features.tg.domain.di import tgExceptionHandlerProvider, tgProvider, \
  tgStateBinderProvider


def handle_exception(_, context):
  ref = storage()
  if 'Unclosed' not in context.get('message', ''):
    exceptionHandler = ref(tgExceptionHandlerProvider)
    exceptionHandler.handle(context['exception'])
  else:
    log: Logger = ref(loggerProvider)
    log.error(f'Unhandled message from asyncio {context}')


async def main():
  asyncio.get_event_loop().set_exception_handler(handle_exception)

  ref = storage()
  tg: AsyncTeleBot = ref(tgProvider)
  config: Config = ref(configProvider)
  binder: TgStateBinder = ref(tgStateBinderProvider)
  log: Logger = ref(loggerProvider)

  locale.setlocale(locale.LC_ALL, config.locale)

  binder.addHandlers()
  await binder.addCommandsToMenu()

  log.info('Bot started')
  await tg.infinity_polling()
  log.info('Bot finished')


if __name__ == '__main__':
  asyncio.run(main())
