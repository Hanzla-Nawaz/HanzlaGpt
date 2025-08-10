import os
import pinecone
from app.core.config import settings

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV)
index = pc.Index(settings.PINECONE_INDEX)

# List all namespaces
stats = index.describe_index_stats()
namespaces = stats.get('namespaces', {})

print(f"\nPinecone Index: {settings.PINECONE_INDEX}")
print(f"Namespaces found: {list(namespaces.keys())}\n")

for ns, ns_stats in namespaces.items():
    print(f"Namespace: {ns}")
    print(f"  Vector count: {ns_stats.get('vector_count', 0)}")
    # Fetch a few sample vectors from this namespace
    try:
        # Query for random vectors (using a zero vector, which will return arbitrary results)
        sample = index.query(vector=[0.0]*stats['dimension'], namespace=ns, top_k=3, include_metadata=True)
        for i, match in enumerate(sample.get('matches', [])):
            print(f"    Sample {i+1}:")
            print(f"      ID: {match.get('id')}")
            print(f"      Metadata: {match.get('metadata')}")
    except Exception as e:
        print(f"    Error fetching samples: {e}")
    print()
