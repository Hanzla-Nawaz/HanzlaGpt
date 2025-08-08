# 🆓 Free AI Providers Guide for HanzlaGPT

This guide covers all the free AI providers integrated into HanzlaGPT for deployment.

## 🎯 Provider Priority Order

1. **OpenAI** (Paid, but most reliable)
2. **Groq** (Free tier: 1000 requests/day)
3. **Together AI** (Free tier: 1000 requests/day)
4. **Replicate** (Free tier: 500 requests/day)
5. **HuggingFace** (Free tier: 30,000 requests/month)
6. **Ollama** (Local, completely free)
7. **Intent-based Fallback** (Local, no API needed)

## 🚀 Free Provider Setup

### 1. **Groq** ⚡ (Fastest Free Option)
- **Website**: https://console.groq.com/
- **Free Tier**: 1000 requests/day
- **Speed**: Very fast (sub-second responses)
- **Models**: Llama 3, Mixtral, Gemma

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
```

**Get API Key:**
1. Go to https://console.groq.com/
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` file

### 2. **Together AI** 🤝 (Reliable Free Option)
- **Website**: https://together.ai/
- **Free Tier**: 1000 requests/day
- **Speed**: Fast (2-5 seconds)
- **Models**: Llama 2, CodeLlama, Mistral

```env
TOGETHER_API_KEY=your_together_api_key_here
TOGETHER_MODEL=meta-llama/Llama-2-7b-chat-hf
```

**Get API Key:**
1. Go to https://together.ai/
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` file

### 3. **Replicate** 🔄 (High-Quality Models)
- **Website**: https://replicate.com/
- **Free Tier**: 500 requests/day
- **Speed**: Medium (5-15 seconds)
- **Models**: Llama 2 70B, CodeLlama, Stable Diffusion

```env
REPLICATE_API_TOKEN=your_replicate_token_here
REPLICATE_MODEL=meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3
```

**Get API Token:**
1. Go to https://replicate.com/
2. Sign up for free account
3. Get API token from dashboard
4. Add to `.env` file

### 4. **HuggingFace** 🤗 (Most Flexible)
- **Website**: https://huggingface.co/
- **Free Tier**: 30,000 requests/month
- **Speed**: Slow (10-30 seconds)
- **Models**: Thousands of open-source models

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

**Get API Token:**
1. Go to https://huggingface.co/
2. Sign up for free account
3. Go to Settings → Access Tokens
4. Create new token
5. Add to `.env` file

### 5. **Ollama** 🦙 (Local, No API Limits)
- **Website**: https://ollama.ai/
- **Cost**: Completely free
- **Speed**: Depends on your hardware
- **Models**: Llama 2, Mistral, CodeLlama

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

**Setup:**
1. Install Ollama: https://ollama.ai/download
2. Run: `ollama pull llama2`
3. Start Ollama service
4. Add to `.env` file

## 📊 Provider Comparison

| Provider | Free Tier | Speed | Quality | Setup Difficulty |
|----------|-----------|-------|---------|------------------|
| **Groq** | 1000/day | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Easy |
| **Together AI** | 1000/day | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Easy |
| **Replicate** | 500/day | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Medium |
| **HuggingFace** | 30K/month | ⚡⚡ | ⭐⭐⭐ | Easy |
| **Ollama** | Unlimited | ⚡⚡⚡ | ⭐⭐⭐⭐ | Hard |
| **Fallback** | Unlimited | ⚡⚡⚡⚡⚡ | ⭐⭐ | None |

## 🛠️ Environment Configuration

### Complete `.env` Example:

```env
# Primary Providers (Paid)
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo

# Free Providers
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama3-8b-8192

TOGETHER_API_KEY=your_together_key_here
TOGETHER_MODEL=meta-llama/Llama-2-7b-chat-hf

REPLICATE_API_TOKEN=your_replicate_token_here
REPLICATE_MODEL=meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3

HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# Local Provider
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Database
PG_HOST=localhost
PG_PORT=5432
PG_USER=your_user
PG_PASSWORD=your_password
PG_DATABASE=hanzlagpt_db

# Vector Store
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_env
PINECONE_INDEX=hanzlagpt-index
PINECONE_NAMESPACE=hanzlagpt-namespace
```

## 🎯 Deployment Strategies

### Strategy 1: Multiple Free Providers
```env
# Use multiple free providers for redundancy
GROQ_API_KEY=your_key
TOGETHER_API_KEY=your_key
HUGGINGFACEHUB_API_TOKEN=your_token
# Comment out OpenAI for free deployment
# OPENAI_API_KEY=
```

### Strategy 2: Local + Cloud
```env
# Use local Ollama + cloud providers
OLLAMA_BASE_URL=http://localhost:11434
GROQ_API_KEY=your_key
HUGGINGFACEHUB_API_TOKEN=your_token
```

### Strategy 3: Cloud-Only
```env
# Use only cloud providers
GROQ_API_KEY=your_key
TOGETHER_API_KEY=your_key
REPLICATE_API_TOKEN=your_token
HUGGINGFACEHUB_API_TOKEN=your_token
```

## 🚀 Installation Commands

### Install Required Packages:

```bash
# Install LangChain providers
pip install langchain-community

# Install specific providers
pip install groq
pip install together
pip install replicate
pip install huggingface-hub

# Install local models
pip install sentence-transformers
```

### For Ollama (Local):
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

## 🧪 Testing Providers

### Test Script:
```bash
python test_provider_accuracy.py
```

### Manual Testing:
1. Set one provider in `.env`
2. Restart backend: `python main.py`
3. Send message in frontend
4. Check provider badge
5. Repeat with different providers

## 📈 Performance Tips

### For Free Tiers:
1. **Use smaller models** for faster responses
2. **Cache responses** to reduce API calls
3. **Implement rate limiting** to stay within limits
4. **Use fallback providers** when limits are reached

### For Deployment:
1. **Monitor API usage** to avoid overages
2. **Set up alerts** for approaching limits
3. **Use multiple providers** for redundancy
4. **Implement graceful degradation**

## 🔧 Troubleshooting

### Common Issues:

1. **Provider not working:**
   - Check API key format
   - Verify account is active
   - Check free tier limits

2. **Slow responses:**
   - Try different models
   - Use local Ollama
   - Check network connection

3. **Provider not switching:**
   - Restart backend
   - Check `.env` file format
   - Verify environment variables

## 🎉 Benefits of Multiple Providers

1. **Redundancy**: If one provider fails, others continue
2. **Cost Optimization**: Use free tiers effectively
3. **Performance**: Choose fastest available provider
4. **Reliability**: Multiple fallback options
5. **Flexibility**: Switch providers based on needs

**Your HanzlaGPT now supports 7 different AI providers with automatic fallback!** 🚀
