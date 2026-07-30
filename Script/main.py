from Embeddings import Embeddings
from DataBase_Connection import Connection
from Storage import Text_Storage
from RAG import Retrieval
from GEMINAI import LLM
def run():
    Embedder = Embeddings()
    embedder = Embedder.get_embbder()
    print("Embeddings are OK")
    connection = Connection()
    collection = connection.get_collection()
    print("DATABASE OK")
    store = Text_Storage(embedder, collection)
    print ("Store OK")
    retrieve = Retrieval(embedder, collection)
    Model = LLM(embedder, collection)
    print("LLM OK")
    
    print("Hello, How can I help you today?")


    while True:
        user_input = input("YOU: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        if user_input.startswith("info:"):
            store.store_text(user_input[6:].strip())
            print("El_3ariff: I got it. Thanks for the info")
        else:    
            retrieved_context = retrieve.retrieve_chunks(user_input)
            answer = Model.ask_rag_system(user_input , retrieved_context)

            print(f"Assistant: {answer}")


            
if __name__ == '__main__':
    run()