# HanzlaGPT Setup Guide 🚀

This guide will help you set up HanzlaGPT with your personal data and get it running with full RAG capabilities.

## 📋 Prerequisites

Before starting, make sure you have:

- Python 3.8+ installed
- PostgreSQL database running
- OpenAI API key
- Pinecone account and API key

## 🛠️ Step-by-Step Setup

### 1. Environment Configuration

Create a `.env` file in the root directory with your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo
OPENAI_API_EMBEDDING_MODEL=text-embedding-3-small

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX=hanzlagpt-index
PINECONE_NAMESPACE=hanzlagpt-namespace

# PostgreSQL Configuration
PG_HOST=localhost
PG_PORT=5432
PG_USER=your_db_user
PG_PASSWORD=your_db_password
PG_DATABASE=hanzlagpt_db

# Social Profiles (Optional)
LINKEDIN_PROFILE=your_linkedin_url
GITHUB_PROFILE=your_github_url
MEDIUM_PROFILE=your_medium_url
KAGGLE_PROFILE=your_kaggle_url
TWITTER_PROFILE=your_twitter_url
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE hanzlagpt_db;
```

The application will automatically create required tables on startup.

### 4. Pinecone Setup

1. Create a Pinecone account at [pinecone.io](https://pinecone.io)
2. Create a new index with:
   - **Dimensions**: 1536 (for text-embedding-3-small)
   - **Metric**: Cosine
   - **Name**: hanzlagpt-index (or your preferred name)

### 5. Load Your Personal Data

Your documents are already in the `app/data` directory. Run the vector loading script:

```bash
python load_vectors.py
```

This will:
- Process all your documents (PDFs, DOCX, TXT files)
- Create embeddings using OpenAI
- Load them into Pinecone with proper metadata
- Show processing statistics

### 6. Test the System

Run the comprehensive test suite:

```bash
python run_tests.py
```

### 7. Start the Application

```bash
python main.py
```

The API will be available at `http://localhost:9090`

### 8. Test the Frontend

Open `frontend/index.html` in your browser to test the chat interface.

## 📊 What Gets Processed

The system will process all documents in your `app/data` directory:

### Document Categories:
- **Resumes & CVs**: Your professional background
- **Certificates**: Technical certifications
- **Certifications**: Professional certifications  
- **Experience Letters**: Work experience documentation
- **Personal Documents**: About me, projects, etc.

### Supported File Types:
- PDF files (resumes, certificates, etc.)
- DOCX files (Word documents)
- TXT files (text documents)
- MD files (markdown documents)

## 🔍 Testing Your Setup

### 1. Health Check
```bash
curl http://localhost:9090/health
```

### 2. Test Chat Query
```bash
curl -X POST http://localhost:9090/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "session_id": "test_session",
    "query": "Tell me about your background and experience"
  }'
```

### 3. Frontend Testing
Open `frontend/index.html` and ask questions like:
- "What are your technical skills?"
- "Tell me about your cybersecurity experience"
- "What certifications do you have?"
- "What projects have you worked on?"

## 🚨 Troubleshooting

### Common Issues:

1. **Missing Environment Variables**
   - Ensure all required variables are set in `.env`
   - Check API keys are valid

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check connection credentials

3. **Pinecone Issues**
   - Verify index exists and is accessible
   - Check API key and environment settings

4. **Document Processing Errors**
   - Check file permissions
   - Ensure documents are readable
   - Verify file formats are supported

### Logs and Debugging:

- Check `logs/hanzlagpt.log` for detailed logs
- Run `python run_tests.py` for comprehensive testing
- Use the health endpoint to check component status

## 🎯 Expected Results

After successful setup, you should be able to:

1. **Ask about your background**: Get detailed responses about your experience
2. **Query your skills**: Get information about your technical expertise
3. **Ask about certifications**: Get details about your professional certifications
4. **Discuss projects**: Get information about your project work
5. **Career guidance**: Get advice based on your experience

## 📈 Performance Tips

1. **Optimize Chunk Size**: Adjust `chunk_size` in `vector_loader.py` for better retrieval
2. **Batch Processing**: The system processes documents in batches to avoid rate limits
3. **Caching**: Responses are cached for better performance
4. **Monitoring**: Check logs for performance metrics

## 🔄 Updating Your Data

To add new documents:

1. Place new files in `app/data/`
2. Run `python load_vectors.py` again
3. The system will process only new documents

## 🎉 Success Indicators

You'll know everything is working when:

- ✅ Vector loading completes without errors
- ✅ API server starts successfully
- ✅ Frontend connects to API
- ✅ Chat responses include your personal information
- ✅ Intent classification works correctly
- ✅ Response times are reasonable (< 5 seconds)

## 📞 Support

If you encounter issues:

1. Check the logs in `logs/hanzlagpt.log`
2. Run the test suite: `python run_tests.py`
3. Verify all environment variables are set
4. Check API key validity and quotas

---

**Your HanzlaGPT is now ready to provide personalized AI assistance based on your expertise and experience!** 🤖✨
