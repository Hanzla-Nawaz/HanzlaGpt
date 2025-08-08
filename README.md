# HanzlaGPT 🤖

A personal AI assistant built with FastAPI, LangChain, and Pinecone that provides intelligent responses based on Hanzala Nawaz's expertise in AI, cybersecurity, and career guidance.

## 🚀 Features

- **Intelligent Intent Detection**: Automatically classifies queries into different categories (career guidance, AI advice, cybersecurity, personal info)
- **RAG (Retrieval-Augmented Generation)**: Uses vector embeddings to provide contextually relevant responses
- **Multi-Modal Responses**: Specialized prompts for different types of questions
- **Chat History**: Persistent conversation tracking with PostgreSQL
- **Production-Ready**: Comprehensive error handling, logging, and monitoring
- **RESTful API**: Clean, documented endpoints with OpenAPI/Swagger support

## 🏗️ Architecture

```
HanzlaGPT/
├── app/
│   ├── api/endpoints/     # FastAPI route handlers
│   ├── core/             # Core functionality (config, database, vectorstore)
│   ├── data/             # Personal data and documents
│   ├── schemas/          # Pydantic models for validation
│   ├── templates/        # LangChain prompts
│   └── utils/            # Utility functions
├── tests/                # Comprehensive test suite
├── data/                 # Personal documents and certificates
├── main.py              # FastAPI application entry point
└── requirements.txt     # Python dependencies
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **AI/ML**: LangChain, OpenAI GPT models
- **Vector Database**: Pinecone
- **Database**: PostgreSQL
- **Document Processing**: pdfplumber, tiktoken
- **Testing**: pytest, pytest-asyncio
- **Logging**: loguru
- **Validation**: Pydantic

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenAI API key
- Pinecone account and API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd HanzlaGPT
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

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

### 3. Database Setup

```sql
-- Create database
CREATE DATABASE hanzlagpt_db;

-- Tables will be created automatically on startup
```

### 4. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:9090
```

### Endpoints

#### Health Check
```http
GET /health
```

#### Root
```http
GET /
```

#### Chat Query
```http
POST /api/chat/query
```

**Request Body:**
```json
{
  "user_id": "string",
  "session_id": "string", 
  "query": "string"
}
```

**Response:**
```json
{
  "response": "string",
  "intent": "string",
  "confidence": 0.9,
  "response_time_ms": 1500
}
```

#### Chat History
```http
GET /api/chat/history/{user_id}/{session_id}?limit=50
```

### Interactive Documentation

- **Swagger UI**: `http://localhost:9090/docs`
- **ReDoc**: `http://localhost:9090/redoc`

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## 🔧 Development

### Code Structure

The application follows clean architecture principles:

- **API Layer**: FastAPI endpoints with proper validation
- **Service Layer**: Business logic and LLM interactions
- **Data Layer**: Database operations and vector store management
- **Core Layer**: Configuration and utility functions

### Adding New Features

1. **New Intent Type**: Add to `app/templates/prompts.py`
2. **New Endpoint**: Create in `app/api/endpoints/`
3. **New Schema**: Add to `app/schemas/schema.py`
4. **New Test**: Add to `tests/`

### Best Practices

- ✅ Use type hints throughout
- ✅ Add comprehensive error handling
- ✅ Write tests for new features
- ✅ Follow PEP 8 style guidelines
- ✅ Use async/await for I/O operations
- ✅ Log important events and errors
- ✅ Validate all inputs with Pydantic

## 📊 Monitoring

The application includes comprehensive logging and monitoring:

- **Request Timing**: Automatic response time tracking
- **Error Tracking**: Detailed error logging with stack traces
- **Health Checks**: Component status monitoring
- **Performance Metrics**: Response times and throughput

## 🔒 Security

- Input validation with Pydantic
- SQL injection prevention with parameterized queries
- CORS configuration
- Trusted host middleware
- Environment variable management

## 🚀 Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 9090

CMD ["python", "main.py"]
```

### Environment Variables

Set all required environment variables in your deployment environment.

### Database Migration

The application automatically creates required tables on startup.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 About Hanzala Nawaz

Hanzala is an AI Engineer and Cybersecurity Analyst with expertise in:
- Machine Learning and AI
- Cybersecurity and GRC
- Data Science and Analytics
- Career Development and Mentorship

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs in `logs/hanzlagpt.log`
3. Run the test suite to verify functionality
4. Create an issue with detailed error information

---

**Built with ❤️ using FastAPI, LangChain, and Pinecone**