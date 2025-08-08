import requests
import json
import time

def test_huggingface_responses():
    """Test HuggingFace responses directly"""
    print("=" * 60)
    print("TESTING HUGGINGFACE RESPONSES")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. CHECKING BACKEND STATUS")
    print("-" * 30)
    try:
        response = requests.get("http://127.0.0.1:8000/api/chat/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status')}")
            print(f"✅ Chat Provider: {data.get('providers', {}).get('chat', {}).get('active')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return
    
    # Test simple chat
    print("\n2. TESTING SIMPLE CHAT")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Hello, what is your name?"
        }
        print("Sending request... (this may take a moment for HuggingFace)")
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Increased timeout for HuggingFace
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('response', 'No response')}")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
            print(f"✅ Intent: {data.get('intent', 'No intent')}")
            print(f"✅ Response Time: {data.get('response_time_ms', 'No time')}ms")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    # Test another question
    print("\n3. TESTING ANOTHER QUESTION")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Tell me about your education"
        }
        print("Sending request... (this may take a moment for HuggingFace)")
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Increased timeout for HuggingFace
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('response', 'No response')}")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    print("\n" + "=" * 60)
    print("HUGGINGFACE RESPONSE TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_huggingface_responses()
