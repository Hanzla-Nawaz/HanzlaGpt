import os
from app.core.config import settings
from app.core.llm_providers import OpenAIProvider
import pinecone

# Path to the all programs file
all_programs_path = os.path.join('app', 'data', 'textdata', 'hanzla_all_programs.txt')

# Read the all programs content
with open(all_programs_path, 'r', encoding='utf-8') as f:
    all_programs_text = f.read()

# Initialize OpenAI embeddings
provider = OpenAIProvider()
embeddings = provider.get_embeddings()
if not embeddings:
    raise RuntimeError('OpenAI embeddings not available. Check your API key.')

# Embed the all programs file
vector = embeddings.embed_query(all_programs_text)

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV)
index = pc.Index(settings.PINECONE_INDEX)

# Upsert the all programs as a single vector in the 'programs' namespace
vector_id = 'hanzla_all_programs'
metadata = {
    'category': 'programs',
    'source': 'hanzla_all_programs.txt',
    'type': 'all_programs_list',
    'text': all_programs_text[:500] + ("..." if len(all_programs_text) > 500 else "")
}
index.upsert(vectors=[{'id': vector_id, 'values': vector, 'metadata': metadata}], namespace='programs')

print(f"Uploaded all programs list to Pinecone 'programs' namespace as ID '{vector_id}'.")
