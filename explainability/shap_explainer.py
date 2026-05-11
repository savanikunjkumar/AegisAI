# Author - Kunjkumar Savani
# MIT2026 Licensee

import numpy as np
# import shap (Simulated for architectural layout)

class AegisSHAPExplainer:
    def __init__(self, model, training_data):
        """
        Initializes the SHAP explainer to interpret complex ML anomaly detectors.
        """
        print("[AegisAI] Initializing SHAP Explainer with base model...")
        self.model = model
        self.training_data = training_data
        # In production: self.explainer = shap.Explainer(self.model, self.training_data)

    def explain_anomaly(self, log_features: np.ndarray, feature_names: list) -> dict:
        """
        Calculates the SHAP values for a specific network log to explain 
        why it was flagged as malicious or anomalous.
        """
        print(f"Generating mathematical proof for anomaly detection...")
        
        # Simulating SHAP values for a flagged log
        # Positive values push the model towards "Threat", negative towards "Safe"
        mock_shap_values = [0.85, -0.12, 0.45, 1.2] 
        
        explanation = {}
        for name, value in zip(feature_names, mock_shap_values):
            impact = "Increased Threat Score" if value > 0 else "Lowered Threat Score"
            explanation[name] = {"shap_value": value, "impact": impact}
            
        # Sort by highest absolute impact
        sorted_explanation = dict(sorted(explanation.items(), key=lambda item: abs(item[1]['shap_value']), reverse=True))
        
        return sorted_explanation

if __name__ == "__main__":
    # Test the Explainer
    explainer = AegisSHAPExplainer(model="Mock_Isolation_Forest", training_data=[])
    features = ["payload_size", "login_frequency", "failed_attempts", "unusual_location"]
    
    # Simulating a log passing through
    results = explainer.explain_anomaly(np.array([10500, 2, 5, 1]), features)
    
    print("\n--- SHAP Threat Explanation ---")
    for feature, data in results.items():
        print(f"Feature: {feature:20} | Impact: {data['impact']:25} | SHAP Value: {data['shap_value']}")
