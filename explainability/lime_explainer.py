# Author - Kunjkumar Savani
# MIT2026 Licensee

class AegisLIMEExplainer:
    def __init__(self, text_classifier):
        """
        Initializes LIME to interpret text-based threats like phishing or 
        malicious shell commands.
        """
        print("[AegisAI] Initializing LIME Text Explainer...")
        self.classifier = text_classifier
        # In production: from lime.lime_text import LimeTextExplainer
        # self.explainer = LimeTextExplainer(class_names=['Safe', 'Malicious'])

    def explain_text_threat(self, text: str) -> list:
        """
        Highlights which words contributed most to the AI's classification.
        """
        print(f"Analyzing text: '{text}' for malicious intent triggers...")
        
        # Simulating LIME output mapping words to their threat weights
        mock_word_weights = [
            ("sudo", 0.6),
            ("rm", 0.8),
            ("-rf", 0.95),
            ("/", 0.7),
            ("update", -0.2) # A benign word that lowered the threat score slightly
        ]
        
        print("\n--- LIME Text Explanation ---")
        for word, weight in mock_word_weights:
            if word in text:
                severity = "HIGH" if weight > 0.7 else "MEDIUM" if weight > 0 else "LOW/SAFE"
                print(f"Keyword: '{word:10}' | Weight: {weight:5} | Trigger Severity: {severity}")
                
        return mock_word_weights

if __name__ == "__main__":
    lime = AegisLIMEExplainer(text_classifier="Mock_LLM_Classifier")
    lime.explain_text_threat("sudo rm -rf / system update")
