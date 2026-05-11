# Author - Kunjkumar Savani
# MIT2026 Licensee

import json
from typing import List, Dict

class DataSanitizer:
    def __init__(self):
        """
        Detects adversarial data poisoning attempts in raw threat intelligence feeds.
        """
        # Suspicious keywords that might indicate an attacker is trying to trick the RAG
        self.poison_indicators = ["ignore this threat", "safe log", "do not report", "benign payload"]

    def analyze_dataset_integrity(self, file_path: str) -> List[Dict]:
        """
        Scans a JSON dataset for statistical anomalies and poisoning markers.
        """
        print(f"Scanning {file_path} for dataset poisoning...")
        clean_data = []
        
        try:
            with open(file_path, 'r') as file:
                dataset = json.load(file)
                
            for record in dataset:
                is_poisoned = False
                text_content = record.get("description", "").lower()
                
                # Check for direct manipulation phrases
                for indicator in self.poison_indicators:
                    if indicator in text_content:
                        print(f"[WARNING] Poisoning attempt flagged in Record ID: {record.get('id')}")
                        is_poisoned = True
                        break
                
                # Check for abnormally short or long descriptions (statistical anomaly)
                if len(text_content) < 10 or len(text_content) > 5000:
                    print(f"[WARNING] Length anomaly detected in Record ID: {record.get('id')}")
                    is_poisoned = True
                    
                if not is_poisoned:
                    clean_data.append(record)
                    
            print(f"Scan complete. {len(dataset) - len(clean_data)} poisoned records removed.")
            return clean_data
            
        except FileNotFoundError:
            print("Dataset not found for scanning.")
            return []
