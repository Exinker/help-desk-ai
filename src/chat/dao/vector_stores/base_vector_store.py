from abc import ABC

from langchain_core.vectorstores import VectorStore


class BaseVectorStoreDAO(ABC):

    @property
    def store(self) -> VectorStore:
        return self._store

    def as_retriever(self, *args, **kwargs) -> None:
        return self.store.as_retriever(*args, **kwargs)
