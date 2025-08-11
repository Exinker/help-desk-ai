from pydantic import Field, computed_field

from config.base_config import BaseConfig


default_system_prompt = '\n'.join([
    'You are an assistant for QA. Use the following pieces of retrieved context to answer the question.',
    'If you don\'t know the answer, just say that you don\'t know.',
    # 'Answer as short as possible.',
    'Context: {context}',
    'Question: {question}',
])
default_k = 5


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
