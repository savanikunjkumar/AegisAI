# Author - Kunjkumar Savani
# MIT2026 Licensee

import os
from rag_pipeline.vector_store.pinecone_client import AegisVectorStore
from llm_security.prompt_templates import AegisPrompts

# Note: In a production environment We would use the official OpenAi library.
# We are mocking the LLM call here to maintain the architectural framework ! 

class MockLLM:
    """A placeholder for OpenAI GPT-4 or an open-source model like Llama-3."""
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        print("\n[AegisAI Processing...]")
        # In reality, this sends the data to the LLM API and waits for the response
        return "Simulated LLM Response: Based on the retrieved CVE data, the vulnerability allows remote code execution. Immediate patching is required."

class AegisSecurityAgent:
    def __init__(self):
        """Initializes the LLM Agent and connects it to the RAG database."""
        self.vector_store = AegisVectorStore()
        self.llm = MockLLM()
        
    # We are simulating the embedding of the user's text question
    def _mock_embed_query(self, query: str) -> list:
        return [0.05] * 1536

    def analyze_threat(self, user_query: str) -> str:
        """
        The core function: 
        1. Embeds the user's question.
        2. Retrieves relevant context from Pinecone.
        3. Sends the context + question to the LLM.
        """
        print(f"Initiating Threat Analysis for query: '{user_query}'")
        
        # 1. Convert question to vector
        query_vector = self._mock_embed_query(user_query)
        
        # 2. Retrieve relevant threat intelligence (Top 3 matches)
        search_results = self.vector_store.query_threats(query_vector=query_vector, top_k=3)
        
        # Extract the text data from the search results
        retrieved_texts = []
        if 'matches' in search_results:
            for match in search_results['matches']:
                if 'metadata' in match and 'text_chunk' in match['metadata']:
                    retrieved_texts.append(match['metadata']['text_chunk'])
        
        context_string = "\n\n".join(retrieved_texts) if retrieved_texts else "No relevant context found in database."
        
        # 3. Prepare the Prompts
        system_prompt = AegisPrompts.get_vulnerability_analyst_prompt()
        final_prompt = AegisPrompts.format_rag_query(user_query, context_string)
        
        # 4. Generate Answer
        response = self.llm.generate_response(system_prompt, final_prompt)
        return response

if __name__ == "__main__":
    # Test the Agent
    agent = AegisSecurityAgent()
    answer = agent.analyze_threat("What are the risks associated with CVE-2024-0001?")
    print("\n--- Final Output ---")
    print(answer)
