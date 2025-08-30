from pydantic import Field, SecretStr

from config.base_config import BaseConfig


class EmbeddingConfig(BaseConfig):

    url: str = Field('http://localhost:11434', alias='EMBEDDING_URL')
    api_key: SecretStr = Field('', alias='EMBEDDING_API_KEY')
    name: str = Field(alias='EMBEDDING_NAME')


EMBEDDING_CONFIG = EmbeddingConfig()
