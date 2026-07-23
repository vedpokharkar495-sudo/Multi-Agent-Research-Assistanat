# config.py
# This file handles all configuration settings

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    # LangSmith Settings
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "Research_Assistant")

    # Model Settings
    MODEL_NAME = "gpt-3.5-turbo"  # You can change to "gpt-4" if available
    TEMPERATURE = 0.7

    # Vector Store Settings
    VECTORSTORE_PATH = "vectorstore/"

    # Documents Path
    DOCUMENTS_PATH = "documents/"

    # Embedding Model
    EMBEDDING_MODEL = "text-embedding-ada-002"

    # Chunk Size for Document Splitting
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200


# Create config instance
config = Config()