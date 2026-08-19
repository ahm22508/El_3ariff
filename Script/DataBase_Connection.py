import chromadb

class Connection:
    def __init__(self):
        self.db = chromadb.PersistentClient(path='./Vector_DataBase')
   
    def get_collection(self):
       self.collection = self.db.get_or_create_collection(name= "PAP_CONFIGURATION_TEAM_DB",
                embedding_function= None,
                configuration={'hnsw' : {'space':'cosine'}},
                metadata={"description": "Internal business knowledge"}
                )
       return self.collection       