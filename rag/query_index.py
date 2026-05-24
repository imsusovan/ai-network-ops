import sys
import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = "rag/chroma_db"
COLLECTION_NAME = "ospf_test_knowledge"


def search(query):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2,
    )

    for doc, metadata in zip(results["documents"][0], results["metadatas"][0], strict=False):
        print("=" * 80)
        print(f"Source: {metadata['source']}")
        print("-" * 80)
        print(doc)


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])

    if not query:
        print("Usage: python rag/query_index.py 'your question'")
        sys.exit(1)

    search(query)
