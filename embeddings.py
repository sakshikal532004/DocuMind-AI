import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")

COLLECTION_NAME = "pdf_chat"

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def create_embeddings(text):

    # Delete old collection so new PDF replaces old PDF data
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    chunk_size = 1000

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    embeddings = model.encode(chunks).tolist()

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )


def retrieve(query):

    try:

        collection = client.get_collection(COLLECTION_NAME)

    except:

        return ""

    embedding = model.encode(query).tolist()

    result = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    docs = result["documents"][0]

    return "\n".join(docs)