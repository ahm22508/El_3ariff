from sentence_transformers import SentenceTransformer

class Embeddings:
    _embedder = None 
   
    @classmethod
    def get_embedder(cls):
        if cls._embedder == None:
            cls._embedder = SentenceTransformer(model_name_or_path= r"C:\El_3ariff\Model\all-MiniLM-L6-v2", local_files_only=True)

        return cls._embedder                                    