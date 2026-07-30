from google import genai
class LLM:
    def __init__(self, embbeder, collection):
        self.client = genai.Client(api_key="AIzaSyAT217LAp6gfdUvsteQnoUHM45LGF9HQ54")
        self.embedder = embbeder
        self.collection = collection




    def ask_rag_system(self ,user_query: str, retrieved_context):
  
        try:

            prompt = f"""You are a helpful assistant. Use ONLY the provided context to answer the user's question. 
                    If the context does not contain the answer, say "I don't have enough information."
                    Context: {retrieved_context}
                    User Question: {user_query}"""

            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            return response.text
        except:
            print("We are working on your request... wait, please")
            self.ask_rag_system(user_query , retrieved_context)