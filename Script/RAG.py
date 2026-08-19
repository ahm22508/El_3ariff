class Retrieval:
    def __init__(self, embedder, collection):
        self.embedder = embedder
        self.collection = collection

    def retrieve_chunks(self, user_input):
        similarity_threshold = 1.0

        if self.collection.count() == 0:
            return []
        query_emb = self.embedder.encode(user_input).tolist()
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=10,
            include=["documents", "distances"]
        )
    
        chunks = []
        for doc, dist in zip(results['documents'][0], results['distances'][0]):
            if dist < similarity_threshold:
                chunks.append(doc)
        return chunks