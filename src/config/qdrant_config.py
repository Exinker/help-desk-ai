from pydantic import Field

from config.base_config import BaseConfig


class QDrantConfig(BaseConfig):

    host: str = Field('localhost', alias='QDRANT_HOST')
    port: int = Field(6333, alias='QDRANT_PORT')


QDRANT_CONFIG = QDrantConfig()
