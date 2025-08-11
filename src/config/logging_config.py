from enum import Enum

from pydantic import Field, field_validator

from config.base_config import BaseConfig


class LoggingLevel(Enum):

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class LoggingConfig(BaseConfig):

    logging_level: LoggingLevel = Field('INFO', alias='LOGGING_LEVEL')

    @field_validator('logging_level', mode='before')
    @classmethod
    def validate_logging_level(cls, value: str) -> LoggingLevel:

        try:
            return LoggingLevel[value]
        except KeyError:
            raise ValueError(f'Logging level {value} is not supported yet!')


LOGGING_CONFIG = LoggingConfig()
