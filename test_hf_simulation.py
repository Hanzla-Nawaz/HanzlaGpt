#!/usr/bin/env python3
"""
Test HuggingFace Fallback Simulation
"""
import os
import requests
import json

def test_hf_simulation():
    """Test HuggingFace fallback by simulating environment"""
    print("=" * 60)
    print("TESTING HUGGINGFACE FALLBACK SIMULATION")
    print("=" * 60)
    
    # Simulate environment variables
    print("\n1. SIMULATING ENVIRONMENT")
    print("-" * 30)
    
    # Set a dummy HuggingFace token for testing
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'hf_test_token_for_fallback'
    # Remove OpenAI key to force fallback
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    print(f"✅ HUGGINGFACEHUB_API_TOKEN: {'Set' if os.getenv('HUGGINGFACEHUB_API_TOKEN') else 'Not set'}")
    print(f"✅ OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    
    # Test health endpoint
    print("\n2. BACKEND HEALTH")
    print("-" * 30)
    try:
        response = requests.get("http://127.0.0.1:8000/api/chat/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Active Chat Provider: {data.get('providers', {}).get('chat', {}).get('active')}")
            print(f"✅ Available Providers: {data.get('providers', {}).get('chat', {}).get('available', [])}")
        else:
            print(f"❌ Health failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test chat query
    print("\n3. TESTING CHAT WITH HF FALLBACK")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Hello, what is your name?"
        }
        print("Sending test query...")
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=60
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
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_hf_simulation()
