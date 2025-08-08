import requests
import json

def test_basic_chat():
    """Test basic chat functionality."""
    
    print("🧪 Testing basic HanzlaGPT functionality...\n")
    
    # Test greeting first
    try:
        print("Testing greeting endpoint...")
        response = requests.get("http://localhost:8000/api/chat/greeting", timeout=10)
        print(f"Greeting status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Greeting works!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Greeting failed: {response.text}")
    except Exception as e:
        print(f"❌ Greeting error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test a simple question
    try:
        print("Testing simple question...")
        data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Hello, can you tell me about yourself?"
        }
        
        response = requests.post(
            "http://localhost:8000/api/chat/query", 
            json=data, 
            timeout=30
        )
        
        print(f"Query status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Query works!")
            print(f"Response: {result.get('response', 'No response')[:300]}...")
            print(f"Intent: {result.get('intent', 'unknown')}")
            print(f"Provider: {result.get('provider', 'unknown')}")
        else:
            print(f"❌ Query failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Query error: {e}")

if __name__ == "__main__":
    test_basic_chat()
