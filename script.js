document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const themeToggle = document.getElementById('theme-toggle');
    const suggestions = document.querySelectorAll('.suggestion');

    // Theme management
    const toggleTheme = () => {
        document.body.classList.toggle('light-mode');
        const icon = themeToggle.querySelector('i');
        if (document.body.classList.contains('light-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            localStorage.setItem('theme', 'light');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            localStorage.setItem('theme', 'dark');
        }
    };

    // Initialize theme
    if (localStorage.getItem('theme') === 'light') {
        toggleTheme();
    }

    themeToggle.addEventListener('click', toggleTheme);

    // Message handling
    const addMessage = (message, isUser = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : 'bot-message';
        
        let avatarIcon, background, alignment, maxWidth;
        
        if (isUser) {
            avatarIcon = '<i class="fas fa-user text-white text-sm"></i>';
            background = 'bg-purple-700';
            alignment = 'items-end justify-end';
            maxWidth = 'ml-auto';
        } else {
            avatarIcon = '<i class="fas fa-robot text-white text-sm"></i>';
            background = 'bg-blue-600';
            alignment = 'items-start';
            maxWidth = '';
        }
        
        messageDiv.innerHTML = `
            <div class="flex ${alignment} gap-3">
                ${isUser ? '' : `
                <div class="w-8 h-8 rounded-full ${background} flex items-center justify-center flex-shrink-0">
                    ${avatarIcon}
                </div>
                `}
                <div class="message-bubble ${isUser ? 'user' : 'bot'} p-4 rounded-lg max-w-[80%] ${maxWidth}">
                    <p>${formatMessage(message)}</p>
                </div>
                ${isUser ? `
                <div class="w-8 h-8 rounded-full ${background} flex items-center justify-center flex-shrink-0">
                    ${avatarIcon}
                </div>
                ` : ''}
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        addCodeCopyFunctionality();
    };

    // Format message with code highlighting
    const formatMessage = (message) => {
        // Simple code block formatting - this could be enhanced with a proper syntax highlighter
        if (message.includes('```')) {
            return message.replace(
                /```(\w*)([\s\S]*?)```/g, 
                (match, language, code) => {
                    return `<pre><button class="code-copy-btn">Copy</button><code class="language-${language || 'plaintext'}">${escapeHtml(code.trim())}</code></pre>`;
                }
            );
        }
        
        // Replace newlines with <br>
        return message.replace(/\n/g, '<br>');
    };
    
    // HTML escape helper
    const escapeHtml = (unsafe) => {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    };

    // Add copy functionality to code blocks
    const addCodeCopyFunctionality = () => {
        document.querySelectorAll('.code-copy-btn').forEach(button => {
            button.addEventListener('click', () => {
                const codeBlock = button.nextElementSibling;
                const code = codeBlock.textContent;
                
                navigator.clipboard.writeText(code).then(() => {
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    button.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
                    
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.style.backgroundColor = '';
                    }, 2000);
                });
            });
        });
    };

    // Automatically scroll to the bottom of the chat
    const scrollToBottom = () => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    // Show loading indicator
    const showLoading = () => {
        loadingIndicator.classList.remove('hidden');
    };

    // Hide loading indicator
    const hideLoading = () => {
        loadingIndicator.classList.add('hidden');
    };

    // Send message to backend
    const sendMessage = async (message) => {
        showLoading();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            const data = await response.json();
            hideLoading();
            return data.response;
        } catch (error) {
            console.error('Error sending message:', error);
            hideLoading();
            throw error;
        }
    };

    // Form submission handler
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        
        // Clear input
        userInput.value = '';
        
        // Get response from backend
        try {
            const response = await sendMessage(message);
            addMessage(response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.');
        }
    });

    // Suggestion click handler
    suggestions.forEach(button => {
        button.addEventListener('click', () => {
            userInput.value = button.textContent;
            userInput.focus();
        });
    });

    // Focus input on page load
    userInput.focus();

    // Initialize with connection to backend
    const initializeConnection = async () => {
        try {
            // In a real app, you might check if the backend is available
            // For now, we'll just add a welcome message
            console.log('Connected to chat backend');
        } catch (error) {
            console.error('Failed to connect to backend:', error);
            addMessage('There was an error connecting to the chat service. Please refresh the page or try again later.');
        }
    };

    // Check connection with the Python backend
    const checkBackendConnection = async () => {
        try {
            const response = await fetch('/health');
            
            if (response.ok) {
                const data = await response.json();
                console.log(`Connected to backend using ${data.provider} model`);
                return true;
            } else {
                throw new Error('Backend health check failed');
            }
        } catch (error) {
            console.error('Error connecting to backend:', error);
            return false;
        }
    };

    // Initialize the app
    initializeConnection();
});