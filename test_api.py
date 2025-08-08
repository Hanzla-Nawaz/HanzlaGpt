import requests
import json

def test_api():
    """Test the API endpoints to identify the issue."""
    
    # Test the query endpoint
    url = "http://localhost:8000/api/chat/query"
    data = {
        "user_id": "test_user",
        "session_id": "test_session", 
        "query": "Hello, can you tell me about yourself?"
    }
    
    try:
        print("Testing API endpoint...")
        response = requests.post(url, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Response: {result}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_api()
