from abc import ABC

from langchain_core.vectorstores import (
    VectorStore,
    VectorStoreRetriever,
)


class BaseVectorStoreDAO(ABC):

    @property
    def store(self) -> VectorStore:
        return self._store

    def as_retriever(self, *args, **kwargs) -> VectorStoreRetriever:
        return self.store.as_retriever(*args, **kwargs)
