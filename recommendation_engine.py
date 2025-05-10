import pandas as pd
import re

# Load mock corpus
corpus = pd.read_json("corpus.json")
documents = corpus.to_dict(orient="records")

def generate_recommendations(query, health_problem, allergies):
    """
    Generate recommendations by matching health problem and allergies in the corpus using keyword-based search.
    """
    try:
        # Normalize inputs
        health_problem = health_problem.lower().strip()
        allergies = allergies.lower().strip() if allergies else ""
        
        # Define keyword synonyms for health problems
        health_keywords = {
            "high blood pressure": ["high blood pressure", "hypertension", "hypertensive"],
            "diabetes": ["diabetes", "diabetic"]
        }
        
        # Find matching health condition
        matched_condition = None
        for condition, synonyms in health_keywords.items():
            if any(keyword in health_problem for keyword in synonyms):
                matched_condition = condition
                break
        
        # Find matching documents
        matched_docs = []
        for doc in documents:
            doc_condition = doc.get("condition", "").lower()
            doc_allergy = doc.get("allergy", "").lower() if doc.get("allergy") else ""
            doc_text = doc.get("text", "")
            
            # Check if document matches health condition
            if matched_condition and matched_condition in doc_condition:
                # Check allergy compatibility
                if not allergies or (allergies and allergies in doc_allergy):
                    matched_docs.append(doc_text)
        
        # Generate response
        if matched_docs:
            response = "Based on your input, here are the recommendations:\n" + "\n".join(matched_docs[:2])  # Limit to 2
        else:
            response = f"No specific recommendations found for '{health_problem}' with '{allergies}' allergy. Try a general diet rich in fruits and vegetables."
        
        return response
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"
