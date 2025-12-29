from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate


class QAChain:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        prompt_template = '''Use the following context from a YouTube video to answer the question.
If you don't know the answer based on the context, say "I don't have enough information from the video to answer that."

Context: {context}

Question: {question}

Answer:'''
        
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    def ask(self, question: str) -> str:
        result = self.chain.invoke({"query": question})
        return result["result"]
