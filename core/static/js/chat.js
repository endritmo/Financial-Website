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
        const loadingEl = appendMessage('Analyzing market data...', 'bot');  // keep loading separate

        try {
            const response = await fetch('/ai/ask/', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();


            // add the real bot response
            loadingEl.remove();
            appendMessage(data.response, 'bot');

            } catch (error) {
            loadingEl.remove();

            appendMessage("Error connecting to AI service.", 'bot');
            }
        chatBody.scrollTop = chatBody.scrollHeight;
    };
    function linkify(text) {
        console.log("RAW TEXT:", text);  // 👈 ADD THIS
        const urlPattern = /(https?:\/\/[^\s]+)/g;

        const result =  text.replace(urlPattern, (url) => {
            console.log("FOUND URL:", url);  // 👈 ADD THIS
            return `<a href="${url}" target="_blank rel="noopener noreferrer style="color: #4ea1ff; text-decoration: underline">🔗 Source</a>`;
        });
        console.log("AFTER LINKIFY:", result);  // 👈 ADD THIS
        return result;
    }
    const appendMessage = (text, sender) => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        //msgDiv.innerText = text;
        msgDiv.innerHTML = linkify(text).replace(/\n/g, "<br>");
        
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        return msgDiv;
    };

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
});
