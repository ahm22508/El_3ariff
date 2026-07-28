import uuid

class Text_Storage:

    def __init__(self, embbeder, collection):
        self.embbeder = embbeder
        self.collection = collection
        

    def store_text(self, text):
        max_words = 300
        words = text.split()
        chunks = []

        if len(words) > max_words:
            for i in range(0, len(words), max_words - 30):
                chunk = " ".join(words[i:i+max_words])
                chunks.append(chunk)
        else:
            chunks.append(text)

        for chunk in chunks:
            emb = self.embbeder.encode(chunk).tolist()
            uid = str(uuid.uuid4())
            self.collection.add(
                documents=[chunk],
                embeddings=[emb],
                ids=[uid]
            )
        