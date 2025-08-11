from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from chat.dao.vector_stores.base_vector_store import BaseVectorStoreDAO
from config import QDRANT_CONFIG


class QdrantVectorStoreDAO(BaseVectorStoreDAO):

    client = QdrantClient(
        host=QDRANT_CONFIG.host,
        port=QDRANT_CONFIG.port,
    )

    def __init__(
        self,
        knowledge_base_id: str,
        embedding: Embeddings,
    ) -> None:

        self._store = QdrantVectorStore(
            client=self.client,
            collection_name=knowledge_base_id,
            embedding=embedding,
        )
