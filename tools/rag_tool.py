# tools/rag_tool.py
# This implements the RAG (Retrieval Augmented Generation) system

import os
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class RAGTool:
    """Tool for document retrieval using RAG"""

    def __init__(self, vectorstore_path: str = "vectorstore/"):
        """
        Initialize the RAG tool

        Args:
            vectorstore_path: Path to store/load vector database
        """
        self.vectorstore_path = vectorstore_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        # Try to load existing vectorstore
        self.load_vectorstore()

    def load_documents(self, document_paths: List[str]) -> None:
        """
        Load and index documents

        Args:
            document_paths: List of paths to documents (PDF, TXT, etc.)
        """
        all_documents = []

        for path in document_paths:
            if path.endswith('.pdf'):
                loader = PyPDFLoader(path)
                documents = loader.load()
                all_documents.extend(documents)
            else:
                # For other file types, read as text
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    from langchain.schema import Document
                    doc = Document(page_content=content)
                    all_documents.append(doc)

        # Split documents
        chunks = self.text_splitter.split_documents(all_documents)

        # Create vectorstore
        self.vectorstore = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        # Save vectorstore
        self.save_vectorstore()

    def save_vectorstore(self) -> None:
        """Save vectorstore to disk"""
        if self.vectorstore:
            os.makedirs(self.vectorstore_path, exist_ok=True)
            self.vectorstore.save_local(self.vectorstore_path)

    def load_vectorstore(self) -> bool:
        """Load vectorstore from disk"""
        try:
            if os.path.exists(self.vectorstore_path):
                self.vectorstore = FAISS.load_local(
                    self.vectorstore_path,
                    self.embeddings
                )
                return True
        except Exception as e:
            print(f"Error loading vectorstore: {e}")
        return False

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """
        Retrieve relevant documents for a query

        Args:
            query: Search query
            k: Number of documents to retrieve

        Returns:
            List of document contents
        """
        if not self.vectorstore:
            # Try to load again
            if not self.load_vectorstore():
                return []

        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []


# Create singleton instance
rag_tool = RAGTool()