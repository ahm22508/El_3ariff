from Embeddings import Embeddings
from DataBase_Connection import Connection
from Storage import Text_Storage
from RAG import Retrieval
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

    
    print("Hello, How can I help you today?")


    while True:
        user_input = input("YOU: ").lower().strip()
        if user_input in ['exit', 'quit']:
            break
        if user_input.startswith("info:"):
            store.store_text(user_input[6:].strip())
            print("El_3ariff: I got it. Thanks for the info")
        else:    
            answer = retrieve.retrieve_chunks(user_input)
            if not answer:
                print("Assistant: I don't know...\n")
            else:
                print(f"Assistant: {"\n".join(answer)}\n")


            
if __name__ == '__main__':
    run()