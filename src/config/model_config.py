from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.base_config import BaseConfig


class ModelConfig(BaseConfig):

    url: str = Field('http://localhost:11434', alias='MODEL_URL')
    api_key: SecretStr = Field('', alias='MODEL_API_KEY')
    name: str = Field(alias='MODEL_NAME')
    temperature: float = Field(0.2, alias='MODEL_TEMPERATURE')


class YandexClientConfig(BaseSettings):

    url: str = Field(alias='YANDEX_CLIENT_URL')
    api_key: SecretStr = Field(alias='YANDEX_CLIENT_API_KEY')
    folder_id: str = Field(alias='YANDEX_CLIENT_FOLDER_ID')
    model_name: str = Field(alias='YANDEX_CLIENT_MODEL_NAME')

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )


MODEL_CONFIG = ModelConfig()
YANDEX_CLIENT_CONFIG = YandexClientConfig()
