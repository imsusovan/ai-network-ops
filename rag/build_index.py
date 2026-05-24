from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


KNOWLEDGE_DIR = Path("knowledge")
DB_DIR = "rag/chroma_db"
COLLECTION_NAME = "ospf_test_knowledge"


def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    docs = []
    ids = []
    metadatas = []

    for file in KNOWLEDGE_DIR.glob("*.md"):
        text = file.read_text()
        docs.append(text)
        ids.append(file.stem)
        metadatas.append({"source": str(file)})

    embeddings = model.encode(docs).tolist()

    collection.upsert(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Indexed {len(docs)} knowledge files")


if __name__ == "__main__":
    main()
