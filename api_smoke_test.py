#!/usr/bin/env python3
"""
Minimal smoke-test of the HanzlaGPT REST API.
Run:  python api_smoke_test.py
"""

import json, time, requests, sys, itertools

BASE = "http://127.0.0.1:8000/api/chat"
headers = {"Content-Type": "application/json"}

def ok(r): return 200 <= r.status_code < 300

def pretty(resp):
    try: return json.dumps(resp.json(), indent=2)[:300]
    except Exception: return resp.text[:300]

def test(name, method, url, **kw):
    print(f"-- {name:30} ", end="", flush=True)
    try:
        r = requests.request(method, url, **kw, timeout=20)
        if ok(r):
            print("PASS")
        else:
            print(f"FAIL {r.status_code}")
            print(pretty(r))
            return
        return r
    except Exception as e:
        print("ERROR", e)

# 1. Health endpoints
test("root /",           "GET", "http://127.0.0.1:8000/")
test("root /health",     "GET", "http://127.0.0.1:8000/health")
test("chat health",      "GET", f"{BASE}/health")

# 2. Greeting
test("greeting",         "GET", f"{BASE}/greeting")

# 3. Query – provider choice & persistence
payload = {"query": "Hi", "user_id": "smoke_user", "provider": "openai"}
test("chat query (openai)","POST",f"{BASE}/query", json=payload, headers=headers)

# second call without provider should retain mapping
payload2 = {"query": "How are you?", "user_id": "smoke_user"}
test("chat query (persist)","POST",f"{BASE}/query", json=payload2, headers=headers)

# 4. Streaming
payload3 = {"query": "Quick greeting", "user_id": "smoke_user", "stream": True}
print("-- stream                         ", end="", flush=True)
with requests.post(f"{BASE}/stream", json=payload3, headers=headers, stream=True) as r:
    if ok(r):
        tokens = "".join(itertools.islice(r.iter_content(decode_unicode=True), 10))
        print("PASS (first tokens ->)", tokens[:80].replace("\n"," "))
    else:
        print("FAIL", r.status_code)

# 5. Provider status / stats
test("provider status",  "GET",  f"{BASE}/provider-status")
test("provider stats",   "GET",  f"{BASE}/provider-stats")

# 6. Force provider (switch to groq if key present, else openai again)
payload_force = {"user_id": "smoke_user", "provider": "openai"}
test("force provider",   "POST", f"{BASE}/force-provider", json=payload_force, headers=headers)

# 7. Metrics
test("chat metrics",     "GET",  f"{BASE}/metrics")

# 8. Cache clear (no json body)
test("cache clear",      "POST", f"{BASE}/cache/clear")

# 9. Debug query
dbg = {"query":"debug me","user_id":"smoke_user"}
test("debug query",      "POST", f"{BASE}/debug/query", json=dbg, headers=headers)

# 10. History
test("chat history",     "GET",
     f"{BASE}/history/smoke_user/{int(time.time())%10000}")   # likely empty

print("\nFinished.")