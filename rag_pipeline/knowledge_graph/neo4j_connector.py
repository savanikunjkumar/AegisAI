# Author - Kunjkumar Savani
# MIT2026 Licensee

import os
from neo4j import GraphDatabase

class AegisKnowledgeGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        """
        Initializes the Neo4j Graph Database connection.
        In a production environment, load these credentials from .env!
        """
        self.uri = os.environ.get("NEO4J_URI", uri)
        self.user = os.environ.get("NEO4J_USER", user)
        self.password = os.environ.get("NEO4J_PASSWORD", password)
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            print("[AegisAI] Successfully connected to Neo4j Knowledge Graph.")
        except Exception as e:
            print(f"[AegisAI] Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def add_threat_relationship(self, actor: str, vulnerability: str, target_system: str):
        """
        Creates a deterministic neural pathway in the graph:
        (ThreatActor) -[EXPLOITS]-> (Vulnerability) -[AFFECTS]-> (System)
        """
        query = """
        MERGE (a:ThreatActor {name: $actor})
        MERGE (v:Vulnerability {cve_id: $vulnerability})
        MERGE (s:System {name: $target_system})
        MERGE (a)-[:EXPLOITS]->(v)
        MERGE (v)-[:AFFECTS]->(s)
        RETURN a.name, v.cve_id, s.name
        """
        
        if not self.driver:
            print("Graph database offline. Cannot add relationship.")
            return
            
        with self.driver.session() as session:
            session.run(query, actor=actor, vulnerability=vulnerability, target_system=target_system)
            print(f"Graph Updated: [{actor}] -> EXPLOITS -> [{vulnerability}] -> AFFECTS -> [{target_system}]")

    def query_vulnerability_impact(self, cve_id: str):
        """
        Retrieves the exact logical mapping of who uses a CVE and what it targets.
        This data is fed directly to the LLM.
        """
        query = """
        MATCH (a:ThreatActor)-[:EXPLOITS]->(v:Vulnerability {cve_id: $cve_id})-[:AFFECTS]->(s:System)
        RETURN a.name AS Actor, s.name AS Target
        """
        
        if not self.driver:
            return "Graph database offline."

        with self.driver.session() as session:
            result = session.run(query, cve_id=cve_id)
            records = [record.data() for record in result]
            return records

if __name__ == "__main__":
    # Test the Neural Graph
    graph = AegisKnowledgeGraph()
    
    # Simulating the ingestion of threat intelligence
    graph.add_threat_relationship(actor="Lazarus Group", vulnerability="CVE-2024-0001", target_system="Windows Server 2022")
    graph.add_threat_relationship(actor="Lazarus Group", vulnerability="CVE-2024-0002", target_system="Linux Kernel 6.1")
    
    # Querying the graph
    impact = graph.query_vulnerability_impact("CVE-2024-0001")
    print(f"\nExtracted Graph Logic for LLM Context: {impact}")
    
    graph.close()
