let employeeId = null;

function toggleChatPopup() {
    const chatPopup = document.getElementById('chat-popup');
    chatPopup.style.display = chatPopup.style.display === 'none' || chatPopup.style.display === '' ? 'flex' : 'none';
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBody = document.getElementById('chat-body');
    const chatFooter = document.querySelector('.chat-footer');

    if (userInput.value.trim() === '') return;

    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = userInput.value;
    chatBody.appendChild(userMessage);

    const message = userInput.value;
    userInput.value = '';

    chatBody.scrollTop = chatBody.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message, employee_id: employeeId })
        });

        const data = await response.json();
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.innerHTML = data.response;
        chatBody.appendChild(botMessage);

        employeeId = data.employee_id;

        chatBody.scrollTop = chatBody.scrollHeight;

        if (data.response.includes("Start New Conversation")) {
            chatFooter.style.display = 'none';
        }

        // Firecracker effect on completion
        if (data.response.includes("Congratulations! You have completed all onboarding tasks.")) {
            showFirecrackers(chatBody);
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

function resetConversation() {
    const chatBody = document.getElementById('chat-body');
    const chatFooter = document.querySelector('.chat-footer');
    chatBody.innerHTML = '';
    employeeId = null;
    chatFooter.style.display = 'flex';
}

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function showFirecrackers(chatBody) {
    for (let i = 0; i < 50; i++) {
        createFirecracker(chatBody);
    }
}

function createFirecracker(chatBody) {
    const firecracker = document.createElement('div');
    firecracker.className = 'firecracker';
    firecracker.style.left = Math.random() * chatBody.offsetWidth + 'px';
    firecracker.style.top = Math.random() * chatBody.offsetHeight + 'px';
    firecracker.style.backgroundColor = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`;
    chatBody.appendChild(firecracker);

    setTimeout(() => {
        firecracker.remove();
    }, 1500); // Remove after 1.5 seconds
}