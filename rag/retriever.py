"""Retrieval helpers for compliance RAG."""

from typing import List

from langchain_core.documents import Document

from rag.vector_store import ComplianceVectorStore


class ComplianceRetriever:
    """Wrapper around FAISS similarity retrieval."""

    def __init__(self) -> None:
        self.vector_store = None

    def refresh(self) -> None:
        """Reload the persisted FAISS index into memory."""

        self.vector_store = ComplianceVectorStore().load_index()

    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """Return top-k relevant rule chunks for a query."""

        if self.vector_store is None:
            self.refresh()
        return self.vector_store.similarity_search(query, k=k)
