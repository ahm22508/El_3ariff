from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self):
        self.Embedder = SentenceTransformer(model_name_or_path= r"C:\El_3ariff\Model\all-MiniLM-L6-v2", 
                                            local_files_only=True)
    def get_embbder(self):
        return self.Embedder
