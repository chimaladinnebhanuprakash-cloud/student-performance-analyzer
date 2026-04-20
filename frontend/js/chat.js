// AI Assistant Chat JavaScript

// Get user session for avatar
let userInitial = 'U';

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChat);
} else {
    initChat();
}

function initChat() {
    // Check if elements exist
    const chatForm = document.getElementById('chatForm');
    if (!chatForm) {
        // Retry after a short delay
        setTimeout(initChat, 100);
        return;
    }

    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('sendBtn');
    const sendBtnText = document.getElementById('sendBtnText');
    const sendBtnLoading = document.getElementById('sendBtnLoading');

    // Get user initial
    getUserInitial();

    // Send message handler
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, true);

        // Clear input
        chatInput.value = '';

        // Show loading
        sendBtnText.classList.add('hidden');
        sendBtnLoading.classList.remove('hidden');
        sendBtn.disabled = true;
        chatInput.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            if (data.success) {
                // Add AI response
                addMessage(data.response, false);
            } else {
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        } catch (error) {
            console.error('Chat error:', error);
            addMessage('Network error. Please check your connection and try again.', false);
        } finally {
            // Hide loading
            sendBtnText.classList.remove('hidden');
            sendBtnLoading.classList.add('hidden');
            sendBtn.disabled = false;
            chatInput.disabled = false;
            chatInput.focus();
        }
    });
}

async function getUserInitial() {
    try {
        const response = await fetch(`${API_BASE}/check-session`, {
            credentials: 'include'
        });
        const data = await response.json();
        if (data.logged_in && data.user.full_name) {
            userInitial = data.user.full_name.charAt(0).toUpperCase();
        }
    } catch (error) {
        console.error('Error getting user initial:', error);
    }
}

// Add message to chat
function addMessage(content, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user' : 'assistant'}`;

    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${isUser ? 'user' : 'assistant'}`;
    avatar.textContent = isUser ? userInitial : 'AI';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
