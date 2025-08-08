import os
import requests
import time

def test_huggingface_fallback_simulation():
    """Test HuggingFace fallback by simulating OpenAI failure"""
    print("=" * 60)
    print("TESTING HUGGINGFACE FALLBACK SIMULATION")
    print("=" * 60)
    
    # Test current state
    print("\n1. CHECKING CURRENT STATE")
    print("-" * 30)
    try:
        response = requests.get("http://127.0.0.1:8000/api/chat/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status')}")
            print(f"✅ Current Chat Provider: {data.get('providers', {}).get('chat', {}).get('active')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return
    
    # Test with a question that might trigger fallback
    print("\n2. TESTING WITH QUESTION THAT MIGHT TRIGGER FALLBACK")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "hf_test_user",
            "session_id": "hf_test_session",
            "query": "Tell me about your education and background in detail"
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('response', 'No response')[:150]}...")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
            print(f"✅ Intent: {data.get('intent', 'No intent')}")
            print(f"✅ Response Time: {data.get('response_time_ms', 'No time')}ms")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    # Test with another question
    print("\n3. TESTING WITH ANOTHER QUESTION")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "hf_test_user",
            "session_id": "hf_test_session",
            "query": "What are your skills and expertise?"
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('response', 'No response')[:150]}...")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    print("\n" + "=" * 60)
    print("HUGGINGFACE FALLBACK SIMULATION COMPLETE")
    print("=" * 60)
    print("\nNOTE: To test HuggingFace fallback, you would need to:")
    print("1. Remove or invalidate the OpenAI API key in .env")
    print("2. Restart the backend")
    print("3. Run this test again")
    print("=" * 60)

if __name__ == "__main__":
    test_huggingface_fallback_simulation()
