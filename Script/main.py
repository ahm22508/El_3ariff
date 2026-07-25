from llama_cpp import Llama 
from sentence_transformers import SentenceTransformer
import chromadb

# Test embedding model
embedder = SentenceTransformer(r"C:\El_3ariff\Model\all-MiniLM-L6-v2",local_files_only=True)
print("Embedding model OK")

# Test Chroma
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="test")
print("Chroma OK")

# Test LLM loading
llm = Llama(model_path=r"C:\El_3ariff\Model\qwen2.5-0.5b.gguf", n_ctx=512, verbose=False)
print("LLM OK")

# Test a simple generation
print("Models loaded!")

while True:
    prompt = input("\nYou: ")
    if prompt.lower() == "exit":
        break
    output = llm(prompt, max_tokens=50)
    print(output['choices'][0]['text'])