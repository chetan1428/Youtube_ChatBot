from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingGenerator:
    def __init__(self):
        # Free local embeddings - no API limits!
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    
    def get_embeddings(self):
        return self.embeddings
