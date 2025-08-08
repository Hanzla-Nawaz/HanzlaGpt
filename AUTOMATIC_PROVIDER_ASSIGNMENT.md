# 🤖 Automatic Provider Assignment System

This document explains how HanzlaGPT automatically assigns different AI providers to different users for optimal load distribution and cost management.

## 🎯 **How It Works**

### **1. User-Based Provider Assignment**
- Each user gets assigned to a specific AI provider
- Same user always gets the same provider (consistency)
- Uses consistent hashing for deterministic assignment
- Automatic fallback if assigned provider fails

### **2. Load Distribution**
- Distributes users across all available providers
- Prevents hitting rate limits on single provider
- Balances load across free tiers
- Automatic rotation every hour for better distribution

### **3. Provider Priority Order**
1. **OpenAI** (Paid, most reliable)
2. **Groq** (1000 requests/day free)
3. **Together AI** (1000 requests/day free)
4. **Replicate** (500 requests/day free)
5. **HuggingFace** (30K requests/month free)
6. **Ollama** (Local, unlimited)
7. **Intent-based Fallback** (Local, no API needed)

## 🚀 **Key Features**

### **✅ Consistent Assignment**
```python
# Same user always gets same provider
user_001 → Groq
user_002 → Together AI
user_003 → Replicate
user_004 → HuggingFace
```

### **✅ Automatic Fallback**
```python
# If Groq fails for user_001
user_001 → Together AI (automatic fallback)
```

### **✅ Load Balancing**
```python
# Distributes users evenly
Provider Distribution:
- Groq: 25% of users
- Together AI: 25% of users
- Replicate: 25% of users
- HuggingFace: 25% of users
```

### **✅ Hourly Rotation**
```python
# Every hour, reassigns users for better distribution
Hour 1: user_001 → Groq
Hour 2: user_001 → Together AI
Hour 3: user_001 → Replicate
```

## 📊 **Provider Statistics**

### **API Endpoints**
```bash
# Get provider statistics
GET /api/chat/provider-stats

# Force provider for user (testing)
POST /api/chat/force-provider?user_id=user_001&provider_name=Groq

# Get current provider status
GET /api/chat/provider-status
```

### **Statistics Response**
```json
{
  "stats": {
    "available_providers": ["OpenAI", "Groq", "Together AI", "HuggingFace"],
    "total_assignments": 150,
    "provider_usage": {
      "OpenAI": 25,
      "Groq": 45,
      "Together AI": 40,
      "Replicate": 20,
      "HuggingFace": 20
    },
    "distribution": {
      "OpenAI": 16.7,
      "Groq": 30.0,
      "Together AI": 26.7,
      "Replicate": 13.3,
      "HuggingFace": 13.3
    },
    "cache_size": 150,
    "last_rotation": 1703123456.789
  }
}
```

## 🧪 **Testing the System**

### **Test Script**
```bash
# Test automatic provider assignment
python test_automatic_provider_assignment.py
```

### **Manual Testing**
```bash
# Test different users
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "session_id": "session_a", "query": "Hello"}'

curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_002", "session_id": "session_b", "query": "Hello"}'
```

## 🎯 **Benefits for Deployment**

### **1. Cost Optimization**
- Uses free tiers effectively
- Distributes load across multiple providers
- Avoids hitting rate limits
- Reduces costs for paid providers

### **2. Reliability**
- Multiple fallback options
- If one provider fails, others continue
- Automatic failover
- Consistent user experience

### **3. Scalability**
- Handles multiple users efficiently
- Load distribution prevents bottlenecks
- Hourly rotation for better balance
- Statistics for monitoring

### **4. User Experience**
- Same provider for same user (consistency)
- Fast response times
- Reliable service
- Transparent provider information

## 🔧 **Configuration**

### **Environment Variables**
```env
# Free Providers (for automatic assignment)
GROQ_API_KEY=your_groq_key
TOGETHER_API_KEY=your_together_key
REPLICATE_API_TOKEN=your_replicate_token
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
OLLAMA_BASE_URL=http://localhost:11434

# Optional: Force specific provider for testing
FORCE_PROVIDER=Groq
```

### **Provider Router Settings**
```python
# In app/core/provider_router.py
rotation_interval = 3600  # Rotate every hour
provider_names = ["OpenAI", "Groq", "Together AI", "Replicate", "HuggingFace", "Ollama"]
```

## 📈 **Monitoring**

### **Provider Usage Dashboard**
```python
# Get real-time statistics
stats = provider_router.get_provider_stats()
print(f"Total users: {stats['total_assignments']}")
print(f"Provider distribution: {stats['distribution']}")
```

### **Health Checks**
```bash
# Check all providers
curl http://localhost:8000/api/chat/provider-status

# Check specific user's provider
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "query": "What provider are you using?"}'
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Provider Not Available**
   ```python
   # Check provider availability
   available = provider_router._get_available_providers()
   print(f"Available: {available}")
   ```

2. **User Getting Different Provider**
   ```python
   # Clear user cache
   provider_router.clear_user_cache("user_id")
   ```

3. **Load Not Distributed**
   ```python
   # Force rotation
   provider_router._rotate_providers()
   ```

### **Debug Commands**
```bash
# Test provider assignment
python test_automatic_provider_assignment.py

# Check provider statistics
curl http://localhost:8000/api/chat/provider-stats

# Force specific provider
curl -X POST "http://localhost:8000/api/chat/force-provider?user_id=test&provider_name=Groq"
```

## 🎉 **Deployment Benefits**

### **For Free Deployment**
- ✅ Uses multiple free providers
- ✅ Distributes load effectively
- ✅ Avoids rate limits
- ✅ Provides redundancy
- ✅ Automatic failover

### **For Paid Deployment**
- ✅ Reduces costs
- ✅ Improves reliability
- ✅ Better user experience
- ✅ Load balancing
- ✅ Monitoring capabilities

**Your HanzlaGPT now automatically assigns the best provider to each user!** 🚀
