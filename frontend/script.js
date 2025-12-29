const API_URL = '';

const youtubeUrlInput = document.getElementById('youtube-url');
const loadBtn = document.getElementById('load-btn');
const videoStatus = document.getElementById('video-status');
const chatBox = document.getElementById('chat-box');
const questionInput = document.getElementById('question-input');
const sendBtn = document.getElementById('send-btn');

let videoLoaded = false;

// Load video
loadBtn.addEventListener('click', async () => {
    const url = youtubeUrlInput.value.trim();
    if (!url) {
        showStatus('Please enter a YouTube URL', 'error');
        return;
    }

    showStatus('Loading video...', '');
    loadBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/load`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok) {
            showStatus('Video loaded successfully!', 'success');
            videoLoaded = true;
            questionInput.disabled = false;
            sendBtn.disabled = false;
            addMessage('Video loaded! You can now ask questions about it.', 'bot');
        } else {
            showStatus(data.detail || 'Failed to load video', 'error');
        }
    } catch (error) {
        showStatus('Error connecting to server', 'error');
    }

    loadBtn.disabled = false;
});

// Send question
sendBtn.addEventListener('click', sendQuestion);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendQuestion();
});

async function sendQuestion() {
    const question = questionInput.value.trim();
    if (!question || !videoLoaded) return;

    addMessage(question, 'user');
    questionInput.value = '';
    sendBtn.disabled = true;

    const loadingMsg = addMessage('Thinking', 'bot');
    loadingMsg.classList.add('loading');

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        loadingMsg.remove();

        if (response.ok) {
            addMessage(data.answer, 'bot');
        } else {
            addMessage('Sorry, I could not process your question.', 'bot');
        }
    } catch (error) {
        loadingMsg.remove();
        addMessage('Error connecting to server.', 'bot');
    }

    sendBtn.disabled = false;
}

function addMessage(text, sender) {
    const msg = document.createElement('div');
    msg.className = `message ${sender}-message`;
    msg.innerHTML = `<p>${text}</p>`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}

function showStatus(text, type) {
    videoStatus.textContent = text;
    videoStatus.className = `status ${type}`;
}
