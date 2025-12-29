# 🎬 YouTube Q&A ChatBot

An AI-powered chatbot that answers questions about any YouTube video using LangChain, Groq, and FAISS vector search.

## Features

- 🎥 Load any YouTube video with captions/transcripts
- 💬 Ask questions about the video content
- ⚡ Fast responses using Groq's Llama 3.1 model
- 🔍 Semantic search with HuggingFace embeddings
- 🎨 Clean, modern dark-themed UI

## Tech Stack

**Backend:**
- FastAPI
- LangChain
- Groq (Llama 3.1 8B)
- HuggingFace Embeddings
- FAISS Vector Store
- YouTube Transcript API

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chetan1428/Youtube_ChatBot.git
cd Youtube_ChatBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in `backend/` folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/keys

## Usage

1. Start the server:
```bash
cd backend
python main.py
```

2. Open your browser and go to:
```
http://localhost:8000
```

3. Paste a YouTube URL and start asking questions!

## Project Structure

```
youtube-qa-bot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── youtube_loader.py    # YouTube transcript loader
│   ├── embedding.py         # HuggingFace embeddings
│   ├── vector_store.py      # FAISS vector database
│   ├── qa_chain.py          # LangChain QA chain
│   └── .env                 # API keys (not in repo)
├── frontend/
│   ├── index.html           # Main UI
│   ├── styles.css           # Styling
│   └── script.js            # Frontend logic
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve frontend UI |
| POST | `/load` | Load YouTube video |
| POST | `/ask` | Ask question about video |
| GET | `/health` | Health check |

## Screenshots

![YouTube Q&A Bot](screenshots/demo.png)

## License

MIT License

## Author

**Chetan** - [GitHub](https://github.com/chetan1428)
