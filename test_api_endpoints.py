import requests
import time

BASE = "http://127.0.0.1:8000"

# Test data
user_id = "apitestuser"
session_id = "apisession1"

print("\n--- Testing POST /api/chat/query (normal chat) ---")
resp = requests.post(f"{BASE}/api/chat/query", json={
    "user_id": user_id,
    "session_id": session_id,
    "query": "Hello, who are you?"
})
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing POST /api/chat/query (user shares name) ---")
resp = requests.post(f"{BASE}/api/chat/query", json={
    "user_id": user_id,
    "session_id": session_id,
    "query": "My name is Ali."
})
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing POST /api/chat/query (ask last question) ---")
resp = requests.post(f"{BASE}/api/chat/query", json={
    "user_id": user_id,
    "session_id": session_id,
    "query": "What was my last question?"
})
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing POST /api/chat/query (unknown intent) ---")
resp = requests.post(f"{BASE}/api/chat/query", json={
    "user_id": user_id,
    "session_id": session_id,
    "query": "Blah blah random text"
})
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing GET /api/chat/history/{user_id}/{session_id} (should show chat history) ---")
resp = requests.get(f"{BASE}/api/chat/history/{user_id}/{session_id}")
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing GET /api/chat/greeting ---")
resp = requests.get(f"{BASE}/api/chat/greeting")
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing GET /api/chat/health ---")
resp = requests.get(f"{BASE}/api/chat/health")
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing POST /api/chat/query (missing fields, should fail) ---")
resp = requests.post(f"{BASE}/api/chat/query", json={
    "user_id": user_id,
    "query": "This should fail"
})
print("Status:", resp.status_code, "Response:", resp.json())

print("\n--- Testing GET /api/chat/history/{user_id}/bad_session (no history) ---")
resp = requests.get(f"{BASE}/api/chat/history/{user_id}/bad_session")
print("Status:", resp.status_code, "Response:", resp.json())
