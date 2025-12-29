from langchain_community.vectorstores import FAISS
from typing import List
from langchain_core.documents import Document


class VectorStore:
    def __init__(self):
        self.db = None
    
    def create_from_documents(self, documents: List[Document], embeddings) -> None:
        self.db = FAISS.from_documents(documents, embeddings)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if self.db is None:
            raise ValueError("Vector store not initialized")
        return self.db.similarity_search(query, k=k)
    
    def as_retriever(self, k: int = 4):
        if self.db is None:
            raise ValueError("Vector store not initialized")
        return self.db.as_retriever(search_kwargs={"k": k})
