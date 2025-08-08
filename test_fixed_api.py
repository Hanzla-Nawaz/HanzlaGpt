import requests
import json

def test_api():
    """Test the API endpoints after fixes."""
    
    print("🧪 Testing HanzlaGPT API after fixes...\n")
    
    # Test greeting
    try:
        print("1. Testing greeting endpoint...")
        response = requests.get("http://localhost:8000/api/chat/greeting", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Greeting works!")
        else:
            print(f"   ❌ Greeting failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Greeting error: {e}")
    
    print()
    
    # Test query
    try:
        print("2. Testing query endpoint...")
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
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Query works!")
            print(f"   Response: {result.get('response', 'No response')[:100]}...")
            print(f"   Intent: {result.get('intent', 'unknown')}")
        else:
            print(f"   ❌ Query failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Query error: {e}")
    
    print()
    
    # Test health (optional)
    try:
        print("3. Testing health endpoint...")
        response = requests.get("http://localhost:8000/api/chat/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check works!")
        else:
            print(f"   ⚠️  Health check failed: {response.text}")
    except Exception as e:
        print(f"   ⚠️  Health check error: {e}")

if __name__ == "__main__":
    test_api()
