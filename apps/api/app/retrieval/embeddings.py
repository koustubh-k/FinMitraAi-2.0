import os
from typing import List, Optional
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding_model() -> Embeddings:
    """
    Factory function to get the embedding model based on configuration.
    """
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
