# Author - Kunjkumar Savani
# MIT2026 Licensee

import os
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any

class AegisVectorStore:
    def __init__(self, index_name: str = "aegis-threat-intel"):
        """
        Initializes the Pinecone connection for the AegisAI RAG pipeline.
        Requires PINECONE_API_KEY to be set in the environment.
        """
        # In a real setup load this from a .env file!
        self.api_key = os.environ.get("PINECONE_API_KEY") 
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY environment variable is missing!")
            
        self.pc = Pinecone(api_key=self.api_key)
        self.index_name = index_name
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)

    def _ensure_index_exists(self):
        """Creates the index if it doesn't already exist for threat data."""
        if self.index_name not in self.pc.list_indexes().names():
            print(f"Creating new Pinecone index: {self.index_name}...")
            self.pc.create_index(
                name=self.index_name,
                dimension=1536, 
                metric="cosine", 
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            print("Index created successfully.")

    def upsert_threat_data(self, vectors: List[Dict[str, Any]]):
        """
        Pushes embedded threat reports (CVEs, logs) into the vector database.
        Format expected: [{"id": "CVE-2024-1234", "values": [0.1, 0.2...], "metadata": {"severity": "HIGH"}}]
        """
        try:
            self.index.upsert(vectors=vectors)
            print(f"Successfully upserted {len(vectors)} threat records to AegisAI Vector Store.")
        except Exception as e:
            print(f"Failed to upsert data: {e}")

    def query_threats(self, query_vector: List[float], top_k: int = 5):
        """Searches the database for the most semantically similar threats."""
        return self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
