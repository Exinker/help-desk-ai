from pydantic import Field, computed_field

from config.base_config import BaseConfig


class OllamaConfig(BaseConfig):

    host: str = Field('localhost', alias='OLLAMA_HOST')
    port: int = Field(11434, alias='OLLAMA_PORT')

    @computed_field
    @property
    def url(self) -> str:
        return 'http://{host}:{port}'.format(
            host=self.host,
            port=self.port,
        )


OLLAMA_CONFIG = OllamaConfig()
