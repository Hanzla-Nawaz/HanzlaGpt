import os
from app.core.config import settings
from app.core.llm_providers import OpenAIProvider
import pinecone

# List of new files to embed and their target namespaces
FILES_TO_EMBED = [
    ("app/data/textdata/hanzla_future_plans.txt", "background"),
    ("app/data/textdata/hanzla_personality_extraversion.txt", "personality"),
    ("app/data/textdata/hanzla_personality_agreeableness.txt", "personality"),
    ("app/data/textdata/hanzla_personality_conscientiousness.txt", "personality"),
    ("app/data/textdata/hanzla_personality_neuroticism.txt", "personality"),
    ("app/data/textdata/hanzla_personality_openness.txt", "personality"),
    ("app/data/textdata/hanzla_professional_programs.txt", "programs"),
]

provider = OpenAIProvider()
embeddings = provider.get_embeddings()
if not embeddings:
    raise RuntimeError('OpenAI embeddings not available. Check your API key.')

pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV)
index = pc.Index(settings.PINECONE_INDEX)

for file_path, namespace in FILES_TO_EMBED:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    vector = embeddings.embed_query(text)
    vector_id = os.path.splitext(os.path.basename(file_path))[0]
    metadata = {
        'category': namespace,
        'source': os.path.basename(file_path),
        'type': 'focused_chunk',
        'text': text[:500] + ("..." if len(text) > 500 else "")
    }
    index.upsert(vectors=[{'id': vector_id, 'values': vector, 'metadata': metadata}], namespace=namespace)
    print(f"Uploaded {file_path} to Pinecone namespace '{namespace}' as ID '{vector_id}'.")
