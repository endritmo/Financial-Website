document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById('ai-toggle-btn');
    const modal = document.getElementById('ai-chat-modal');
    const closeBtn = document.getElementById('close-chat');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatBody = document.getElementById('chat-body');

    toggleBtn.addEventListener('click', () => modal.classList.toggle('hidden'));
    closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

    const sendMessage = async () => {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        chatInput.value = '';
        const loadingId = appendMessage('Analyzing market data...', 'bot');

        try {
            const response = await fetch('/ai/ask/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            document.getElementById(loadingId).innerText = data.response;
        } catch (error) {
            document.getElementById(loadingId).innerText = "Error connecting to AI service.";
        }
        chatBody.scrollTop = chatBody.scrollHeight;
    };

    const appendMessage = (text, sender) => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.innerText = text;
        const id = 'msg-' + Date.now();
        msgDiv.id = id;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        return id;
    };

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
});
