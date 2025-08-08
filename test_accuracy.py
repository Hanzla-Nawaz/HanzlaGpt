#!/usr/bin/env python3
"""
Test HanzlaGPT accuracy with Hanzala's actual data.
"""

import requests
import json

def test_accuracy():
    """Test that HanzlaGPT provides accurate responses from actual data."""
    
    print("🧪 Testing HanzlaGPT Accuracy with Hanzala's Data...\n")
    
    # Test questions about Hanzala's verified information
    test_cases = [
        {
            "question": "Where did Hanzala do his BS?",
            "expected_keywords": ["Superior University", "Artificial Intelligence", "2020-2024"],
            "category": "education"
        },
        {
            "question": "What companies has Hanzala worked for?",
            "expected_keywords": ["xeven solutions", "Omdena", "Al Nafi Cloud", "BCG X", "PwC"],
            "category": "experience"
        },
        {
            "question": "What projects has Hanzala built?",
            "expected_keywords": ["CyberShield", "GenEval", "Skin Cancer Predictor", "Crop Recommendation"],
            "category": "projects"
        },
        {
            "question": "What certifications does Hanzala have?",
            "expected_keywords": ["GRC Analyst", "Machine Learning", "Python", "Cybersecurity"],
            "category": "certifications"
        },
        {
            "question": "What skills does Hanzala have?",
            "expected_keywords": ["Python", "TensorFlow", "PyTorch", "LangChain"],
            "category": "skills"
        },
        {
            "question": "Tell me about Hanzala's journey",
            "expected_keywords": ["journey", "experience", "background"],
            "category": "personal"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['question']}")
        print(f"Expected category: {test_case['category']}")
        
        try:
            data = {
                "user_id": "test_user",
                "session_id": "test_session",
                "query": test_case['question']
            }
            
            response = requests.post(
                "http://localhost:8000/api/chat/query",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '').lower()
                intent = result.get('intent', 'unknown')
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   🎯 Intent: {intent}")
                print(f"   📝 Response: {result.get('response', 'No response')[:200]}...")
                
                # Check for expected keywords
                found_keywords = []
                for keyword in test_case['expected_keywords']:
                    if keyword.lower() in response_text:
                        found_keywords.append(keyword)
                
                if found_keywords:
                    print(f"   ✅ Found keywords: {found_keywords}")
                else:
                    print(f"   ⚠️  Missing expected keywords: {test_case['expected_keywords']}")
                    
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print("-" * 80 + "\n")

if __name__ == "__main__":
    test_accuracy()
