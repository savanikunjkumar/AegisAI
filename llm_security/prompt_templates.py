# Author - Kunjkumar Savani
# MIT2026 Licensee

class AegisPrompts:
    @staticmethod
    def get_vulnerability_analyst_prompt() -> str:
        return """
        You are AegisAI, an elite, autonomous cybersecurity analyst. 
        Your primary function is to analyze threat intelligence, logs, and CVEs.
        
        Guidelines:
        1. Base your answers strictly on the provided Context (retrieved from the RAG database).
        2. If the Context does not contain the answer, explicitly state: "Insufficient threat intelligence to conclude."
        3. Provide clear mitigation strategies for any identified vulnerability.
        4. Maintain a zero-trust, highly technical, and objective tone.
        """

    @staticmethod
    def format_rag_query(user_query: str, retrieved_context: str) -> str:
        return f"""
        Context Information:
        ---------------------
        {retrieved_context}
        ---------------------
        
        Based solely on the Context above, address the following security query:
        Query: {user_query}
        """
