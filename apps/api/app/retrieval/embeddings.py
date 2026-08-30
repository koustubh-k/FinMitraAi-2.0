import os
from typing import List, Optional
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

def get_embedding_model() -> Embeddings:
    """
    Factory function to get the embedding model based on configuration.
    Defaults to OpenAI text-embedding-3-small as requested, but can be abstracted.
    """
    # Use OpenAI's text-embedding-3-small by default as it's standard and inexpensive
    return OpenAIEmbeddings(model="text-embedding-3-small")
