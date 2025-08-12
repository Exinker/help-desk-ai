import logging
from collections.abc import Mapping, Sequence
from typing import Self

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
from langchain_mistralai import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings

from chat.dao.vector_stores import QdrantVectorStoreDAO
from config import (
    MODEL_CONFIG,
    OLLAMA_CONFIG,
)


LOGGER = logging.getLogger(__name__)


CHAT = ChatMistralAI(
    api_key=MODEL_CONFIG.api_key,
    model_name=MODEL_CONFIG.model_name,
    temperature=MODEL_CONFIG.temperature,
)
# EMBEDDING = MistralAIEmbeddings(
#     model=MODEL_CONFIG.embed_name,
#     api_key=MODEL_CONFIG.api_key,
# )
EMBEDDING = OllamaEmbeddings(
    base_url=OLLAMA_CONFIG.url,
    model=MODEL_CONFIG.embed_name,
)


class Service:

    @classmethod
    def create(
        cls,
        system_prompt: str,
        knowledge_base_id: str,
        k: int,
    ) -> Self:

        vector_store = QdrantVectorStoreDAO(
            knowledge_base_id=knowledge_base_id,
            embedding=EMBEDDING,
        )
        retriever = vector_store.as_retriever(
            search_kwargs={'k': k},
        )

        chain = RunnableParallel(
            context=RunnableLambda(lambda data: data['question']) | retriever | cls.format_documents,
            history=lambda data: cls.format_history(data['history']),
            question=lambda data: data['question'],
        ) | ChatPromptTemplate([
            ('system', system_prompt),
        ]) | CHAT | StrOutputParser()

        return Service(
            chain=chain,
        )

    def __init__(
        self,
        chain: Runnable,
    ) -> None:

        self._chain = chain

    @property
    def chain(self) -> Runnable:
        return self._chain

    @staticmethod
    def format_history(history: Sequence[Mapping[str, str]]) -> str:

        return '\n'.join([
            f'{role}: {content}'
            for record in history
            for role, content in record.items()
        ])

    @staticmethod
    def format_documents(documents: Sequence[Document]) -> str:

        return '\n'.join([
            document.page_content
            for document in documents
        ])
