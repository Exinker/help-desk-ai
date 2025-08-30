import logging
from collections.abc import Mapping, Sequence
from typing import Self

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
from langchain_mistralai import ChatMistralAI
from langchain_ollama.embeddings import OllamaEmbeddings

from chat.dao.vector_stores import QdrantVectorStoreDAO
from config import (
    EMBEDDING_CONFIG,
    MODEL_CONFIG,
)


LOGGER = logging.getLogger(__name__)


CHAT = ChatMistralAI(
    api_key=MODEL_CONFIG.api_key,
    model_name=MODEL_CONFIG.name,
    temperature=MODEL_CONFIG.temperature,
)
embedding = OllamaEmbeddings(
    model=EMBEDDING_CONFIG.name,
)


class Service:

    @classmethod
    def create(
        cls,
        system_prompt: str,
        retrieve_prompt: str,
        knowledge_base_id: str,
        k: int,
    ) -> Self:

        vector_store = QdrantVectorStoreDAO(
            knowledge_base_id=knowledge_base_id,
            embedding=embedding,
        )
        retriever = vector_store.as_retriever(
            search_kwargs={'k': k},
        )

        retrieve_chain = RunnableParallel(
            query=RunnableLambda(lambda data: data['question']) | ChatPromptTemplate([('system', retrieve_prompt)]) | CHAT | StrOutputParser(),
            history=lambda data: cls.format_history(data['history']),
        ) | RunnableParallel(
            context=RunnableLambda(lambda data: data['query']) | retriever | cls.format_documents,
            history=lambda data: data['history'],
            query=lambda data: data['query'],
        ) | ChatPromptTemplate([
            ('system', system_prompt),
        ]) | CHAT | StrOutputParser()

        return Service(
            retrieve_chain=retrieve_chain,
        )

    def __init__(
        self,
        retrieve_chain: Runnable,
    ) -> None:

        self._retrieve_chain = retrieve_chain

    @property
    def retrieve_chain(self) -> Runnable:
        return self._retrieve_chain

    @staticmethod
    def format_history(history: Sequence[Mapping[str, str]]) -> str:

        return '\n'.join([
            f'{role}: {content}'
            for record in history
            for role, content in record.items()
        ])

    @staticmethod
    def format_documents(documents: Sequence[Document]) -> str:

        return '\n\n'.join([
            '\n'.join([
                'Headers: {}'.format('/'.join(document.metadata['headers'])),
                'Summary: {}'.format(document.metadata['summary']),
                'Content: {}'.format(document.page_content),
            ])
            for document in documents
        ])
