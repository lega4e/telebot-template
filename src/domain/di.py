import json
import logging
import sys

from lega4e_library import provider, Storage

from src.domain.models.config import Config, LogConfig


@provider
def configProvider(_: Storage):
  if len(sys.argv) < 2:
    raise Exception('No config file was provided')
  return Config.fromJson(json.load(open(sys.argv[1], 'r')))


@provider
def loggerProvider(ref: Storage) -> logging.Logger:
  config: LogConfig = configProvider(ref).log

  class LogStream:

    def write(self, report):
      if config.replaceNewLine:
        report = str(report).strip().replace('\n', '\u0085') + '\n'
      sys.stdout.write(str(report))
      sys.stdout.flush()

  formatter = logging.Formatter(fmt=config.fmt, datefmt=config.datefmt)
  handler = logging.StreamHandler()
  handler.setFormatter(formatter)
  handler.setStream(LogStream())

  logger = logging.getLogger('system')
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)

  return logger
