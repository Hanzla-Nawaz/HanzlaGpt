# HanzlaGPT Deployment Guide 🚀

This guide covers deploying HanzlaGPT with multiple LLM providers and fallback strategies for various hosting platforms.

## 🎯 Deployment Options

### 1. **Vercel (Recommended for Free Tier)**
- **Pros**: Free tier, easy deployment, automatic scaling
- **Cons**: Serverless limitations, cold starts
- **Best for**: Personal projects, demos

### 2. **Railway/Render**
- **Pros**: Free tier, easy deployment, good performance
- **Cons**: Limited free tier resources
- **Best for**: Small to medium projects

### 3. **Docker + Cloud Providers**
- **Pros**: Full control, scalable, portable
- **Cons**: More complex setup, costs
- **Best for**: Production deployments

### 4. **Local Deployment**
- **Pros**: Full control, no costs, privacy
- **Cons**: Requires local resources
- **Best for**: Development, testing

## 🔧 LLM Provider Configuration

### Primary Providers (in order of preference):

1. **OpenAI** (Paid, but reliable)
2. **HuggingFace** (Free tier available)
3. **Ollama** (Local, free)
4. **Local Embeddings** (Free, local)

### Environment Variables Setup:

```env
# Required for all deployments
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX=hanzlagpt-index
PINECONE_NAMESPACE=hanzlagpt-namespace

# Database (choose one)
# Option 1: PostgreSQL (recommended)
PG_HOST=your_db_host
PG_PORT=5432
PG_USER=your_db_user
PG_PASSWORD=your_db_password
PG_DATABASE=hanzlagpt_db

# Option 2: SQLite (for simple deployments)
DATABASE_URL=sqlite:///./hanzlagpt.db

# Free alternatives
HUGGINGFACE_API_KEY=your_hf_key_here  # Optional
OLLAMA_BASE_URL=http://localhost:11434  # For local Ollama
OLLAMA_MODEL=llama2  # Model to use with Ollama

# Social profiles (optional)
LINKEDIN_PROFILE=your_linkedin_url
GITHUB_PROFILE=your_github_url
MEDIUM_PROFILE=your_medium_url
```

## 🚀 Deployment Methods

### Method 1: Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Set Environment Variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add PINECONE_API_KEY
   # ... add all required variables
   ```

4. **Deploy with environment**:
   ```bash
   vercel --prod
   ```

### Method 2: Railway Deployment

1. **Connect GitHub repository** to Railway
2. **Add environment variables** in Railway dashboard
3. **Deploy automatically** on push

### Method 3: Docker Deployment

1. **Build image**:
   ```bash
   docker build -t hanzlagpt .
   ```

2. **Run container**:
   ```bash
   docker run -p 9090:9090 \
     -e OPENAI_API_KEY=your_key \
     -e PINECONE_API_KEY=your_key \
     hanzlagpt
   ```

3. **Docker Compose** (for full stack):
   ```yaml
   version: '3.8'
   services:
     hanzlagpt:
       build: .
       ports:
         - "9090:9090"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - PINECONE_API_KEY=${PINECONE_API_KEY}
       depends_on:
         - postgres
     
     postgres:
       image: postgres:13
       environment:
         POSTGRES_DB: hanzlagpt_db
         POSTGRES_USER: hanzlagpt_user
         POSTGRES_PASSWORD: hanzlagpt_pass
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

### Method 4: Local Deployment

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up local database**:
   ```bash
   # Install PostgreSQL or use SQLite
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 🔄 Fallback Strategy

The system automatically handles fallbacks:

1. **OpenAI fails** → **HuggingFace** (free)
2. **HuggingFace fails** → **Ollama** (local)
3. **All fail** → **Simple keyword matching**

### Testing Fallbacks:

```bash
# Test with OpenAI disabled
OPENAI_API_KEY="" python main.py

# Test with specific provider
HUGGINGFACE_API_KEY="your_key" python main.py
```

## 📊 Free Tier Limits

### Vercel:
- **Functions**: 100GB-hours/month
- **Bandwidth**: 100GB/month
- **Duration**: 10 seconds max

### Railway:
- **CPU**: 0.5 vCPU
- **RAM**: 512MB
- **Storage**: 1GB

### HuggingFace:
- **API calls**: 30,000/month (free)
- **Models**: Limited selection

## 🛠️ Optimization for Free Tiers

### 1. **Reduce Model Size**:
```python
# In app/core/llm_providers.py
self.chat_model_name = "microsoft/DialoGPT-small"  # Smaller model
self.embedding_model_name = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # Smaller embeddings
```

### 2. **Optimize Chunk Size**:
```python
# In vector_loader.py
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Smaller chunks
    chunk_overlap=50,  # Less overlap
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```

### 3. **Use SQLite for Database**:
```python
# In app/core/config.py
DATABASE_URL = "sqlite:///./hanzlagpt.db"
```

### 4. **Cache Responses**:
```python
# Add caching to reduce API calls
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_response(query: str):
    # Your response logic here
    pass
```

## 🔍 Monitoring and Debugging

### Health Check Endpoint:
```bash
curl https://your-app.vercel.app/health
```

### Provider Status:
```json
{
  "status": "healthy",
  "providers": {
    "chat_provider": "OpenAI",
    "embedding_provider": "OpenAI",
    "providers": {
      "OpenAI": {"available": true, "chat_model": true, "embeddings": true},
      "HuggingFace": {"available": true, "chat_model": true, "embeddings": true}
    }
  }
}
```

### Logs:
- **Vercel**: `vercel logs`
- **Railway**: Dashboard logs
- **Docker**: `docker logs container_name`

## 🚨 Troubleshooting

### Common Issues:

1. **Cold Start Delays**:
   - Use Vercel Pro for better performance
   - Implement response caching

2. **Memory Limits**:
   - Reduce model sizes
   - Use smaller embeddings

3. **API Rate Limits**:
   - Implement exponential backoff
   - Use multiple providers

4. **Database Connection Issues**:
   - Use connection pooling
   - Implement retry logic

### Debug Commands:

```bash
# Test provider availability
python -c "from app.core.llm_providers import provider_manager; print(provider_manager.get_provider_status())"

# Test vector store
python -c "from app.core.vectorstore import create_vector_store; print(create_vector_store())"

# Test data loading
python load_vectors.py
```

## 📈 Scaling Considerations

### For Production:

1. **Use Paid Providers**:
   - OpenAI for reliability
   - Pinecone for vector storage
   - PostgreSQL for database

2. **Implement Caching**:
   - Redis for response caching
   - CDN for static assets

3. **Add Monitoring**:
   - Application performance monitoring
   - Error tracking
   - Usage analytics

4. **Security**:
   - API key rotation
   - Rate limiting
   - Input validation

## 🎉 Success Indicators

Your deployment is successful when:

- ✅ Health check returns "healthy"
- ✅ All providers are available
- ✅ Vector store is accessible
- ✅ Chat responses are generated
- ✅ Response times are < 5 seconds
- ✅ No errors in logs

## 📞 Support

For deployment issues:

1. **Check logs** for specific errors
2. **Test locally** first
3. **Verify environment variables**
4. **Check provider availability**
5. **Monitor resource usage**

---

**Your HanzlaGPT is now ready for deployment with robust fallback strategies!** 🚀✨
