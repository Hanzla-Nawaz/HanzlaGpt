import os
import requests
import time

def test_huggingface_simple():
    """Simple test to verify HuggingFace fallback"""
    print("=" * 50)
    print("TESTING HUGGINGFACE FALLBACK")
    print("=" * 50)
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:8000/api/chat/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running")
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Chat Provider: {data.get('providers', {}).get('chat', {}).get('active')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return
    
    # Test chat with HuggingFace fallback
    print("\nTesting chat with HuggingFace fallback...")
    try:
        chat_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Hello, what is your name?"
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('response', 'No response')[:100]}...")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
            print(f"✅ Intent: {data.get('intent', 'No intent')}")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    test_huggingface_simple()
