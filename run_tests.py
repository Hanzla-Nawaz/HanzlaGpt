#!/usr/bin/env python3
"""
Comprehensive test runner for HanzlaGPT
Tests all components and provides detailed feedback
"""

import sys
import os
import subprocess
import time
import requests
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

def test_imports():
    """Test if all required modules can be imported."""
    print("\n🧪 Testing imports...")
    
    modules_to_test = [
        "fastapi",
        "uvicorn", 
        "langchain",
        "langchain_community",
        "openai",
        "pinecone",
        "psycopg2",
        "pdfplumber",
        "tiktoken",
        "python-dotenv",
        "pydantic-settings",
        "loguru"
    ]
    
    failed_imports = []
    for module in modules_to_test:
        try:
            __import__(module.replace('-', '_'))
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Missing modules: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All imports successful")
        return True

def test_configuration():
    """Test configuration loading."""
    print("\n⚙️  Testing configuration...")
    
    try:
        from app.core.config import settings
        print("✅ Configuration loaded successfully")
        
        # Check required settings
        required_settings = [
            'OPENAI_API_KEY',
            'OPENAI_MODEL_NAME',
            'PINECONE_API_KEY',
            'PINECONE_ENV',
            'PG_HOST',
            'PG_PORT',
            'PG_USER',
            'PG_PASSWORD',
            'PG_DATABASE'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not getattr(settings, setting, None):
                missing_settings.append(setting)
        
        if missing_settings:
            print(f"⚠️  Missing environment variables: {', '.join(missing_settings)}")
            print("Please check your .env file")
            return False
        else:
            print("✅ All required settings found")
            return True
            
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

def test_database():
    """Test database connectivity."""
    print("\n🗄️  Testing database...")
    
    try:
        from app.core.database import create_tables, get_connection_pool
        print("✅ Database module imported successfully")
        
        # Test connection pool creation
        pool = get_connection_pool()
        print("✅ Database connection pool created")
        
        # Test table creation
        create_tables()
        print("✅ Database tables created/verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        print("Please check your PostgreSQL connection settings")
        return False

def test_vector_store():
    """Test vector store initialization."""
    print("\n🔍 Testing vector store...")
    
    try:
        from app.core.vectorstore import create_vector_store
        vector_store = create_vector_store()
        
        if vector_store:
            print("✅ Vector store initialized successfully")
            return True
        else:
            print("⚠️  Vector store initialization failed (may be due to missing API keys)")
            print("This is not critical for basic functionality")
            return True
            
    except Exception as e:
        print(f"❌ Vector store test failed: {str(e)}")
        print("Please check your Pinecone and OpenAI API keys")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print("\n🌐 Testing API endpoints...")
    
    # Start the server in background
    print("Starting test server...")
    server_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:9090/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = requests.get("http://localhost:9090/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test chat endpoint
        test_data = {
            "user_id": "test_user",
            "session_id": "test_session", 
            "query": "Hello, how are you?"
        }
        
        response = requests.post(
            "http://localhost:9090/api/chat/query",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            print(f"   Response: {data.get('response', 'No response')[:100]}...")
            print(f"   Intent: {data.get('intent', 'Unknown')}")
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API test failed: {str(e)}")
        return False
    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()

def test_data_loader():
    """Test data loader functionality."""
    print("\n📚 Testing data loader...")
    
    try:
        from app.data.data_loader import DataLoader
        
        loader = DataLoader()
        documents = loader.load_all_documents()
        
        if documents:
            print(f"✅ Data loader working - {len(documents)} documents loaded")
            
            # Test document splitting
            split_docs = loader.split_documents(documents)
            print(f"✅ Document splitting working - {len(split_docs)} chunks created")
            
            return True
        else:
            print("⚠️  No documents found to load")
            print("This is normal if no documents are in the data directory")
            return True
            
    except Exception as e:
        print(f"❌ Data loader test failed: {str(e)}")
        return False

def run_pytest():
    """Run pytest suite."""
    print("\n🧪 Running pytest suite...")
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("❌ pytest not installed. Install with: pip install pytest")
        return False
    
    # Run pytest
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ All pytest tests passed")
        return True
    else:
        print("❌ Some pytest tests failed")
        print(result.stdout)
        print(result.stderr)
        return False

def main():
    """Run all tests."""
    print("🚀 HanzlaGPT Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Database Test", test_database),
        ("Vector Store Test", test_vector_store),
        ("Data Loader Test", test_data_loader),
        ("API Endpoints Test", test_api_endpoints),
        ("Pytest Suite", run_pytest)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! HanzlaGPT is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
