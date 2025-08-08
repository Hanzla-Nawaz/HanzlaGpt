#!/usr/bin/env python3
"""
Debug HuggingFace Fallback
"""
import os
import sys
import requests
import json

def test_provider_status():
    """Test the current provider status"""
    print("=" * 60)
    print("DEBUGGING HUGGINGFACE FALLBACK")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. ENVIRONMENT VARIABLES")
    print("-" * 30)
    openai_key = os.getenv('OPENAI_API_KEY')
    hf_key = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    print(f"✅ OPENAI_API_KEY: {'Set' if openai_key else 'Not set'}")
    print(f"✅ HUGGINGFACEHUB_API_TOKEN: {'Set' if hf_key else 'Not set'}")
    
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
    
    # Test a simple query to see what happens
    print("\n3. TESTING CHAT QUERY")
    print("-" * 30)
    try:
        chat_data = {
            "user_id": "debug_user",
            "session_id": "debug_session", 
            "query": "Hello, what is your name?"
        }
        print("Sending test query...")
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/query",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=30
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
    print("DEBUG COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_provider_status()
