import os
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from youtube_loader import YouTubeVideoLoader
from embedding import EmbeddingGenerator
from vector_store import VectorStore
from qa_chain import QAChain

load_dotenv()

app = FastAPI(title="YouTube Q&A Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

vector_store = None
qa_chain = None
video_title = None


class VideoRequest(BaseModel):
    url: str


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


@app.post("/load")
async def load_video(request: VideoRequest):
    global vector_store, qa_chain, video_title
    
    try:
        loader = YouTubeVideoLoader()
        video_data = loader.load(request.url)
        video_title = video_data["title"]
        
        embedding_gen = EmbeddingGenerator()
        
        vector_store = VectorStore()
        vector_store.create_from_documents(
            video_data["chunks"],
            embedding_gen.get_embeddings()
        )
        
        qa_chain = QAChain(vector_store)
        
        return {
            "success": True,
            "message": "Video loaded successfully",
            "title": video_title
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    global qa_chain
    
    if qa_chain is None:
        raise HTTPException(status_code=400, detail="No video loaded")
    
    try:
        answer = qa_chain.ask(request.question)
        return {"answer": answer}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "video_loaded": vector_store is not None,
        "video_title": video_title
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
