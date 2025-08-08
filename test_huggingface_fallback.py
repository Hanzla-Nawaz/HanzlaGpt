import os
import requests

def test_huggingface_fallback():
    """Test HuggingFace fallback when OpenAI is not available"""
    print("=" * 60)
    print("TESTING HUGGINGFACE FALLBACK")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. CHECKING ENVIRONMENT VARIABLES")
    print("-" * 30)
    hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    print(f"✅ HUGGINGFACEHUB_API_TOKEN: {'Set' if hf_token else 'Not set'}")
    print(f"✅ OPENAI_API_KEY: {'Set' if openai_key else 'Not set'}")
    
    # Test health endpoint to see current provider
    print("\n2. CHECKING CURRENT PROVIDER")
    print("-" * 30)
    try:
        response = requests.get("http://127.0.0.1:8000/api/chat/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Chat Provider: {data.get('providers', {}).get('chat', {}).get('active')}")
            print(f"✅ Embedding Provider: {data.get('providers', {}).get('embeddings', {}).get('active')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test chat with HuggingFace fallback
    print("\n3. TESTING CHAT WITH HUGGINGFACE")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "hf_test_user",
            "session_id": "hf_test_session",
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
            print(f"✅ Response: {data.get('response', 'No response')[:200]}...")
            print(f"✅ Intent: {data.get('intent', 'No intent')}")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
            print(f"✅ Response Time: {data.get('response_time_ms', 'No time')}ms")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    # Test another question
    print("\n4. TESTING ANOTHER QUESTION")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "hf_test_user",
            "session_id": "hf_test_session",
            "query": "Tell me about your education"
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('response', 'No response')[:200]}...")
            print(f"✅ Provider: {data.get('provider', 'No provider')}")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    print("\n" + "=" * 60)
    print("HUGGINGFACE FALLBACK TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_huggingface_fallback()
