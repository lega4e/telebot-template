from lega4e_library import provider, Storage
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from tgui.src.logging.exception_handler import TgExceptionHandler
from tgui.src.logging.tg_logger import TgLogger
from tgui.src.managers.callback_query_manager import CallbackQueryManager
from tgui.src.managers.tg_state_binder import Command, TgStateBinder

from src.domain.di import configProvider, loggerProvider
from src.domain.models.config import Config
from src.features.tg.domain.user_scope import UserScope


@provider
def tgProvider(ref: Storage):
  config: Config = ref(configProvider)
  return AsyncTeleBot(
    token=config.tg.token,
    exception_handler=ref(tgExceptionHandlerProvider),
  )


@provider
def tgExceptionHandlerProvider(ref: Storage):
  return TgExceptionHandler(ref(loggerProvider))


@provider
def callbackQueryManagerProvider(ref: Storage):
  return CallbackQueryManager(ref(loggerProvider))


@provider
def tgLoggerProvider(ref: Storage):
  config: Config = ref(configProvider)
  return TgLogger(
    tgLoggerName='tglog',
    tg=ref(tgProvider),
    tgFmt=config.log.fmt,
    tgTimestampFmt=config.log.datefmt,
    tgIgnoreList=[],
    chats=[],
    systemLogger=ref(loggerProvider),
  )


@provider
def tgStateBinderProvider(ref: Storage):

  def stateGetter(m: Message):
    return None if m.chat.id < 0 else ref(UserScope, tgId=m.chat.id).root

  return TgStateBinder(
    commands=[
      Command(
        name='/menu',
        preview='menu',
        description='Меню',
        addToMenu=True,
      ),
    ],
    tg=ref(tgProvider),
    logger=ref(tgLoggerProvider),
    stateGetter=stateGetter,
    callbackQueryManager=ref(callbackQueryManagerProvider),
    ignoreGroups=True,
  )
