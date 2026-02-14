"""FAISS vector store management for compliance rules."""

from __future__ import annotations

from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import get_settings


class ComplianceVectorStore:
    """Builds and loads a FAISS index for compliance policies."""

    def __init__(self) -> None:
        self.settings = get_settings()
        # TODO: Set GOOGLE_API_KEY in your .env file.
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=self.settings.gemini_embedding_model,
            google_api_key=self.settings.google_api_key,
        )

    def _load_rule_text(self, rule_file_path: Path | None = None) -> str:
        rule_path = rule_file_path or self.settings.compliance_rules_path
        return rule_path.read_text(encoding="utf-8")

    def build_index(self, rule_file_path: Path | None = None) -> None:
        """Build and persist FAISS index from compliance rule text."""

        text = self._load_rule_text(rule_file_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        chunks = splitter.split_text(text)

        docs: List[Document] = [
            Document(page_content=chunk, metadata={"source": "compliance_rules"}) for chunk in chunks
        ]
        db = FAISS.from_documents(docs, self.embeddings)
        db.save_local(str(self.settings.vector_store_dir))

    def load_index(self) -> FAISS:
        """Load persisted FAISS index from disk."""

        return FAISS.load_local(
            str(self.settings.vector_store_dir),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
