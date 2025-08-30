from pydantic import Field, SecretStr

from config.base_config import BaseConfig


class ModelConfig(BaseConfig):

    url: str = Field('http://localhost:11434', alias='MODEL_URL')
    api_key: SecretStr = Field('', alias='MODEL_API_KEY')
    name: str = Field(alias='MODEL_NAME')
    temperature: float = Field(0.2, alias='MODEL_TEMPERATURE')


MODEL_CONFIG = ModelConfig()
