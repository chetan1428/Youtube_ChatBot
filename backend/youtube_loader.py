from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import re


class YouTubeVideoLoader:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def extract_video_id(self, url: str) -> str:
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Invalid YouTube URL")
    
    def load(self, url: str) -> dict:
        video_id = self.extract_video_id(url)
        
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        
        full_text = " ".join([item.text for item in transcript_list])
        
        doc = Document(page_content=full_text, metadata={"source": url, "video_id": video_id})
        chunks = self.text_splitter.split_documents([doc])
        
        return {
            "title": f"Video {video_id}",
            "url": url,
            "chunks": chunks,
            "metadata": {"video_id": video_id}
        }
