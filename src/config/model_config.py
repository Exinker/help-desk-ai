from pydantic import Field, SecretStr

from config.base_config import BaseConfig


class ModelConfig(BaseConfig):

    api_key: SecretStr = Field(alias='MODEL_API_KEY')
    base_url: str = Field(alias='MODEL_URL')
    model_name: str = Field(alias='MODEL_GENERATION_NAME')
    embed_name: str = Field(alias='MODEL_EMBEDDING_NAME')
    temperature: float = Field(0.3, alias='MODEL_TEMPERATURE')


MODEL_CONFIG = ModelConfig()
