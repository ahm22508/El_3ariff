from sentence_transformers import SentenceTransformer
import chromadb
import uuid


embedder = SentenceTransformer(r"C:\El_3ariff\Model\all-MiniLM-L6-v2",local_files_only=True)
print("Embedding model OK")

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="test")
print("Chroma OK")

def store_teach(text):
    """Store a new fact (auto split if too long)."""
    max_words = 300
    words = text.split()
    # Split into chunks of max_words, with 30 word overlap
    if len(words) > max_words:
        chunks = []
        for i in range(0, len(words), max_words - 30):
            chunk = " ".join(words[i:i+max_words])
            chunks.append(chunk)
    else:
        chunks = [text]

    for chunk in chunks:
        emb = embedder.encode(chunk).tolist()
        uid = str(uuid.uuid4())
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[uid]
        )
        

def retrieve_chunks(query, n_results=10, similarity_threshold = 1.50):
    """Find the most relevant stored chunks for a query."""
    if collection.count() == 0:
        return []
    query_emb = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=n_results,
        include=["documents", "distances"]
    )
   
    chunks = []
    for doc, dist in zip(results['documents'][0], results['distances'][0]):
        print(doc)
        print(dist)
        if dist < similarity_threshold:
            chunks.append(doc)
    return chunks





print("Private Business Assistant ready.")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break

    if user_input.startswith("info:"):
        fact = user_input[6:].strip()
        if fact:
            store_teach(fact)
            print("Assistant: Got it. I've saved that information.\n")
        else:
            print("Assistant: Please provide the information after TEACH:.\n")
        continue

    chunks = retrieve_chunks(user_input)
    if not chunks:
        print("Assistant: I don't know...\n")
    else:
        print(f"Assistant: {"\n".join(chunks)}\n")