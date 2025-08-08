import requests
import time

def test_server():
    """Test if the HanzlaGPT server is running and responding."""
    
    # Test basic health endpoint
    try:
        print("Testing server health...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test chat greeting endpoint
    try:
        print("\nTesting chat greeting...")
        response = requests.get("http://localhost:8000/api/chat/greeting", timeout=10)
        print(f"Greeting status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Greeting test failed: {e}")
    
    # Test chat query endpoint
    try:
        print("\nTesting chat query...")
        data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Hello, can you tell me about your AI experience?"
        }
        response = requests.post("http://localhost:8000/api/chat/query", json=data, timeout=30)
        print(f"Query status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Query test failed: {e}")

if __name__ == "__main__":
    print("Testing HanzlaGPT server...")
    test_server()
