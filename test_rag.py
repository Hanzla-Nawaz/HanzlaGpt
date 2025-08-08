import requests
import json

def test_hanzala_data():
    """Test if HanzlaGPT can respond from Hanzala's actual data."""
    
    # Test questions about Hanzala's specific information
    test_questions = [
        "What is Hanzala's educational background?",
        "Where did Hanzala do his BS?",
        "What certifications does Hanzala have?",
        "What projects has Hanzala worked on?",
        "What is Hanzala's journey in AI?",
        "What companies has Hanzala worked for?",
        "What skills does Hanzala have?",
        "Tell me about Hanzala's GitHub repositories",
        "What was Hanzala's experience at Omdena?",
        "What cybersecurity experience does Hanzala have?"
    ]
    
    print("🧪 Testing HanzlaGPT with Hanzala's actual data...\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        
        try:
            data = {
                "user_id": "test_user",
                "session_id": "test_session",
                "query": question
            }
            
            response = requests.post(
                "http://localhost:8000/api/chat/query", 
                json=data, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"🎯 Intent: {result.get('intent', 'unknown')}")
                print(f"📝 Response: {result.get('response', 'No response')[:200]}...")
                print(f"⏱️  Response Time: {result.get('response_time_ms', 0)}ms")
                print(f"🤖 Provider: {result.get('provider', 'unknown')}")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 80 + "\n")

if __name__ == "__main__":
    test_hanzala_data()
