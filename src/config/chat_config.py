from pydantic import Field

from config.base_config import BaseConfig


default_system_prompt = '\n'.join([
    'You are an assistant for QA. Use the following pieces of retrieved context to answer the question.',
    'If you don\'t know the answer, just say that you don\'t know.',
    # 'Answer as short as possible.',
    'Context: {context}',
    'Question: {question}',
])
default_k = 5


class ChatConfig(BaseConfig):

    system_prompt: str = Field(default_system_prompt, alias='CHAT_SYSTEM_PROMPT')
    knowledge_base_id: str = Field(alias='CHAT_KNOWLEDGE_BASE_ID')
    k: int = Field(default_k, alias='CHAT_KNOWLEDGE_BASE_K')


CHAT_CONFIG = ChatConfig()
