# Author - Kunjkumar Savani
# MIT2026 Licensee

import json
from vector_store.pinecone_client import AegisVectorStore

# to convert text into actual 1536-dimensional vectors. For the architectural skeleton, 
# we will simulate the embedding process Furthur !!

def embed_text(text: str) -> list:
    """
    Mock function to simulate an LLM embedding model.
    In production, replace this with OpenAIEmbeddings or HuggingFace BGE.
    """
    # Returns a dummy vector of 1536 dimensions
    return [0.01] * 1536 

def ingest_cve_dataset(filepath: str):
    """
    Reads a local JSON file of CVEs and pushes them into the Pinecone RAG database.
    """
    print(f"Starting ingestion process for {filepath}...")
    
    try:
        with open(filepath, 'r') as file:
            cve_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}. Please add sample data.")
        return

    vector_store = AegisVectorStore()
    vectors_to_upsert = []

    for cve in cve_data:
        # 1. Create a rich text representation for the AI to understand
        content_to_embed = f"Vulnerability: {cve['id']}. Description: {cve['description']}. Severity: {cve['severity']}."
        
        # 2. Convert text to vector
        vector_embedding = embed_text(content_to_embed)
        
        # 3. Format for Pinecone with metadata so the LLM can filter by severity later
        vectors_to_upsert.append({
            "id": cve["id"],
            "values": vector_embedding,
            "metadata": {
                "severity": cve["severity"],
                "text_chunk": content_to_embed # Store the text so the LLM can read it upon retrieval
            }
        })

    # Push to the database
    vector_store.upsert_threat_data(vectors_to_upsert)

if __name__ == "__main__":
    # Test the pipeline with local dummy data
    ingest_cve_dataset("../data/cve_samples/sample_cves.json")
