from attr.validators import instance_of
from attrs import define, field
from lega4e_library.attrs.jsonkin import jsonkin, Jsonkin


@jsonkin
@define
class TgConfig(Jsonkin):
  token: str = field(validator=instance_of(str))
  name: str = field(validator=instance_of(str))


@jsonkin
@define
class DbConfig(Jsonkin):
  host: str = field(validator=instance_of(str))
  port: str = field(validator=instance_of(str))
  user: str = field(validator=instance_of(str))
  password: str = field(validator=instance_of(str))
  name: str = field(validator=instance_of(str))


@jsonkin
@define
class LogConfig(Jsonkin):
  fmt: str = field(validator=instance_of(str))
  datefmt: str = field(validator=instance_of(str))
  replaceNewLine: bool = field(validator=instance_of(bool))


@jsonkin
@define
class Config(Jsonkin):
  locale: str = field(validator=instance_of(str))
  tg: TgConfig = TgConfig.attrField()
  db: DbConfig = DbConfig.attrField()
  log: LogConfig = LogConfig.attrField()
