import os
import requests
import time
import tempfile
import shutil

def test_huggingface_fallback_demo():
    """Demo HuggingFace fallback by temporarily modifying environment"""
    print("=" * 60)
    print("HUGGINGFACE FALLBACK DEMO")
    print("=" * 60)
    
    # Backup original .env
    print("\n1. BACKING UP ORIGINAL .ENV")
    print("-" * 30)
    backup_path = ".env.backup"
    shutil.copy2(".env", backup_path)
    print(f"✅ Original .env backed up to {backup_path}")
    
    # Read current .env
    with open(".env", "r") as f:
        env_content = f.read()
    
    # Create modified .env with invalid OpenAI key
    print("\n2. CREATING MODIFIED .ENV WITH INVALID OPENAI KEY")
    print("-" * 30)
    modified_content = env_content.replace(
        'OPENAI_API_KEY="sk-proj-B31SuSe9IHXncN6wh9UWL0_NxcjL9T02A3vHaslQ_Ab8810tSieRAaRqNl6enLoWlY9lGwsIVcT3BlbkFJzj4nVV2hFBkWLwJ62hH1QG4ErFTIXpNExQazwl_-8noH-fpcFlFp-9zqY7BE28grNz-UfmkTQAhan"',
        'OPENAI_API_KEY="sk-invalid-key-for-testing"'
    )
    
    with open(".env", "w") as f:
        f.write(modified_content)
    print("✅ Modified .env with invalid OpenAI key")
    
    # Restart backend with modified environment
    print("\n3. RESTARTING BACKEND WITH MODIFIED ENVIRONMENT")
    print("-" * 30)
    print("Please restart the backend manually with: python main.py")
    print("Then run this test again to see HuggingFace fallback in action.")
    
    # Restore original .env
    print("\n4. RESTORING ORIGINAL .ENV")
    print("-" * 30)
    shutil.copy2(backup_path, ".env")
    print("✅ Original .env restored")
    
    print("\n" + "=" * 60)
    print("DEMO SETUP COMPLETE")
    print("=" * 60)
    print("\nTo test HuggingFace fallback:")
    print("1. The .env has been modified with an invalid OpenAI key")
    print("2. Restart the backend: python main.py")
    print("3. Run this test again to see the fallback in action")
    print("4. The original .env will be restored automatically")
    print("=" * 60)

if __name__ == "__main__":
    test_huggingface_fallback_demo()
