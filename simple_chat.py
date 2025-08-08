#!/usr/bin/env python3
"""
Simple HanzlaGPT - A working version that responds from Hanzala's data
without complex vector store setup.
"""

import requests
import json
import time

def simple_hanzala_response(query: str) -> str:
    """Simple response system based on Hanzala's actual data."""
    
    query_lower = query.lower()
    
    # Hanzala's actual information
    hanzala_data = {
        "education": {
            "degree": "B.S. in Artificial Intelligence",
            "university": "Superior University",
            "years": "2020-2024"
        },
        "experience": {
            "omdena": "Machine Learning Engineer at Omdena (Nov 2023–Mar 2024)",
            "al_nafi": "Cybersecurity Analyst at Al Nafi Cloud (Jan 2022–Aug 2022)",
            "bcg": "Data Science Intern at BCG X (Feb 2022–Mar 2022)",
            "pwc": "Cybersecurity Intern at PwC Switzerland (Jan 2022–Mar 2022)"
        },
        "projects": {
            "cybershield": "AI-based Cybersecurity Management System with real-time anomaly detection",
            "geneval": "Generative Content Evaluation Library for text, image & video evaluation",
            "skin_cancer": "Skin Cancer Predictor with 86% classification accuracy using CNN",
            "crop_recommendation": "Crop Recommendation System with 99% accuracy",
            "spacex": "SpaceX Falcon 9 Landing Predictor with 87% accuracy"
        },
        "certifications": [
            "GRC Analyst",
            "Introduction to Cybersecurity Tools & Cyber Attacks",
            "Generative AI for Everyone",
            "Intermediate Python",
            "Machine Learning - Supervised Learning",
            "Machine Learning - Unsupervised Learning",
            "Python (Primer, Alpha, Beta)",
            "R Programming",
            "ISO 27001, ISO 27017, ISO 27018 Lead",
            "Linux Level 1",
            "RHEL Intensive"
        ],
        "skills": [
            "Python", "SQL", "Git", "TensorFlow", "PyTorch", "LangChain",
            "scikit-learn", "OpenAIEmbeddings", "Pinecone", "FAISS",
            "Cybersecurity tools", "Docker", "Streamlit", "Gradio", "FastAPI"
        ],
        "journey": "Started with no programming knowledge, learned from scratch, now expert in AI/ML and cybersecurity"
    }
    
    # Simple keyword matching
    if any(word in query_lower for word in ["education", "degree", "university", "bs", "bachelor"]):
        return f"Hanzala completed his {hanzala_data['education']['degree']} from {hanzala_data['education']['university']} ({hanzala_data['education']['years']})."
    
    elif any(word in query_lower for word in ["experience", "work", "job", "company", "omdena", "al nafi", "bcg", "pwc"]):
        return f"Hanzala's work experience includes: {hanzala_data['experience']['omdena']}, {hanzala_data['experience']['al_nafi']}, {hanzala_data['experience']['bcg']}, and {hanzala_data['experience']['pwc']}."
    
    elif any(word in query_lower for word in ["project", "cybershield", "geneval", "skin cancer", "crop", "spacex"]):
        return f"Hanzala's key projects include: {hanzala_data['projects']['cybershield']}, {hanzala_data['projects']['geneval']}, {hanzala_data['projects']['skin_cancer']}, {hanzala_data['projects']['crop_recommendation']}, and {hanzala_data['projects']['spacex']}."
    
    elif any(word in query_lower for word in ["certification", "certificate", "cert"]):
        return f"Hanzala has {len(hanzala_data['certifications'])} certifications including: {', '.join(hanzala_data['certifications'][:5])} and many more."
    
    elif any(word in query_lower for word in ["skill", "technology", "programming"]):
        return f"Hanzala's skills include: {', '.join(hanzala_data['skills'][:10])} and more."
    
    elif any(word in query_lower for word in ["journey", "story", "background", "start"]):
        return f"Hanzala's journey: {hanzala_data['journey']}. He started with no programming knowledge and worked hard to become an expert in AI/ML and cybersecurity."
    
    else:
        return "Hi! I'm Hanzala Nawaz, an AI and cybersecurity expert. I completed my BS in AI from Superior University and have worked at companies like Omdena, Al Nafi Cloud, BCG X, and PwC. I have expertise in machine learning, cybersecurity, and data science. How can I help you?"

def test_simple_hanzala():
    """Test the simple HanzalaGPT responses."""
    
    test_questions = [
        "What is Hanzala's educational background?",
        "Where did Hanzala do his BS?",
        "What companies has Hanzala worked for?",
        "What projects has Hanzala worked on?",
        "What certifications does Hanzala have?",
        "What skills does Hanzala have?",
        "Tell me about Hanzala's journey"
    ]
    
    print("🧪 Testing Simple HanzalaGPT...\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        response = simple_hanzala_response(question)
        print(f"Response: {response}")
        print("-" * 80 + "\n")

if __name__ == "__main__":
    test_simple_hanzala()
