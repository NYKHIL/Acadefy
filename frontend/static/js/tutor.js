/**
 * Acadefy Tutor JavaScript
 * Handles AI chat functionality and real-time interactions
 */

class AcadefyTutor {
    constructor() {
        this.sessionId = window.AcadefyApp.sessionId;
        this.messageCount = 0;
        this.sessionStartTime = new Date();
        this.isTyping = false;
        this.messageHistory = [];
        
        this.init();
    }
    
    init() {
        console.log('Initializing AI tutor...');
        this.setupEventListeners();
        this.updateSessionInfo();
        this.loadChatHistory();
        this.focusInput();
    }
    
    setupEventListeners() {
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const fileInput = document.getElementById('chat-file-input');
        
        if (messageInput) {
            // Auto-resize textarea
            messageInput.addEventListener('input', () => {
                this.autoResizeTextarea(messageInput);
                this.updateCharacterCount();
                this.toggleSendButton();
            });
            
            // Send message on Enter (but not Shift+Enter)
            messageInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            // Update character count
            this.updateCharacterCount();
        }
        
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleChatFileUpload(e));
        }
        
        // Setup quick action buttons
        this.setupQuickActions();
    }
    
    setupQuickActions() {
        const quickActions = document.querySelectorAll('.quick-action');
        quickActions.forEach(action => {
            action.addEventListener('click', (e) => {
                const message = e.currentTarget.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
                if (message) {
                    this.insertQuickMessage(message);
                }
            });
        });
        
        const subjectButtons = document.querySelectorAll('.subject-btn');
        subjectButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const message = e.currentTarget.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
                if (message) {
                    this.insertQuickMessage(message);
                }
            });
        });
    }
    
    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px';
    }
    
    updateCharacterCount() {
        const messageInput = document.getElementById('message-input');
        const charCount = document.getElementById('char-count');
        
        if (messageInput && charCount) {
            const count = messageInput.value.length;
            charCount.textContent = count;
            
            // Change color if approaching limit
            if (count > 900) {
                charCount.style.color = 'var(--danger-color)';
            } else if (count > 800) {
                charCount.style.color = 'var(--warning-color)';
            } else {
                charCount.style.color = 'var(--gray-500)';
            }
        }
    }
    
    toggleSendButton() {
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        
        if (messageInput && sendButton) {
            const hasText = messageInput.value.trim().length > 0;
            sendButton.disabled = !hasText || this.isTyping;
            
            if (hasText && !this.isTyping) {
                sendButton.style.background = 'var(--primary-color)';
            } else {
                sendButton.style.background = 'var(--gray-300)';
            }
        }
    }
    
    async sendMessage() {
        const messageInput = document.getElementById('message-input');
        if (!messageInput || this.isTyping) return;
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Clear input and update UI
        messageInput.value = '';
        this.autoResizeTextarea(messageInput);
        this.updateCharacterCount();
        this.toggleSendButton();
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to API
            const response = await window.AcadefyApp.apiRequest('/tutor', {
                method: 'POST',
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            if (response.success) {
                // Add AI response to chat
                this.addMessage(response.data.response, 'ai');
                
                // Update session info
                this.messageCount += 2; // User message + AI response
                this.updateSessionInfo();
                
                // Store in message history
                this.messageHistory.push({
                    user: message,
                    ai: response.data.response,
                    timestamp: new Date().toISOString()
                });
                
                // Save to local storage
                this.saveChatHistory();
                
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'ai', true);
                this.showErrorModal(response.error);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection and try again.', 'ai', true);
        } finally {
            this.hideTypingIndicator();
        }
    }
    
    addMessage(content, type, isError = false) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}-message`;
        
        const timestamp = window.AcadefyApp.formatTimeAgo(new Date());
        
        // Handle system messages differently
        if (type === 'system') {
            messageElement.innerHTML = `
                <div class="system-message-content">
                    <i class="fas fa-info-circle"></i>
                    <span>${content}</span>
                </div>
            `;
        } else {
            messageElement.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-${type === 'user' ? 'user' : 'robot'}"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble ${isError ? 'error-message' : ''}">
                        <p>${this.formatMessageContent(content)}</p>
                    </div>
                    <div class="message-time">${timestamp}</div>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageElement);
        
        // Animate message appearance
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            messageElement.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        }, 50);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    formatMessageContent(content) {
        // Basic formatting for AI responses
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/`(.*?)`/g, '<code>$1</code>') // Inline code
            .replace(/\n/g, '<br>'); // Line breaks
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        this.toggleSendButton();
        
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'flex';
            this.scrollToBottom();
        }
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        this.toggleSendButton();
        
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'none';
        }
    }
    
    scrollToBottom() {
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            setTimeout(() => {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 100);
        }
    }
    
    updateSessionInfo() {
        // Update message count
        const messageCountElement = document.getElementById('message-count');
        if (messageCountElement) {
            messageCountElement.textContent = this.messageCount;
        }
        
        // Update session ID display
        const sessionIdElement = document.getElementById('session-id');
        if (sessionIdElement) {
            sessionIdElement.textContent = this.sessionId.substring(0, 8) + '...';
        }
        
        // Update session start time
        const sessionStartElement = document.getElementById('session-start');
        if (sessionStartElement) {
            sessionStartElement.textContent = window.AcadefyApp.formatTimeAgo(this.sessionStartTime);
        }
    }
    
    insertQuickMessage(message) {
        const messageInput = document.getElementById('message-input');
        if (messageInput) {
            messageInput.value = message;
            messageInput.focus();
            this.autoResizeTextarea(messageInput);
            this.updateCharacterCount();
            this.toggleSendButton();
        }
    }
    
    async loadChatHistory() {
        try {
            const response = await window.AcadefyApp.apiRequest(`/tutor/history/${this.sessionId}`);
            
            if (response.success && response.data.history) {
                const history = response.data.history;
                
                // Clear existing messages except welcome message
                const chatMessages = document.getElementById('chat-messages');
                const welcomeMessage = chatMessages?.querySelector('.message.ai-message');
                if (chatMessages) {
                    chatMessages.innerHTML = '';
                    if (welcomeMessage) {
                        chatMessages.appendChild(welcomeMessage);
                    }
                }
                
                // Add historical messages
                history.forEach(interaction => {
                    this.addMessage(interaction.user_message, 'user');
                    this.addMessage(interaction.ai_response, 'ai');
                });
                
                this.messageCount = history.length * 2;
                this.updateSessionInfo();
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    saveChatHistory() {
        window.AcadefyApp.storage.set('chat_history', this.messageHistory);
    }
    
    clearChat() {
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            // Keep only the welcome message
            const welcomeMessage = chatMessages.querySelector('.message.ai-message');
            chatMessages.innerHTML = '';
            if (welcomeMessage) {
                chatMessages.appendChild(welcomeMessage);
            }
        }
        
        this.messageHistory = [];
        this.messageCount = 0;
        this.updateSessionInfo();
        this.saveChatHistory();
        
        window.AcadefyApp.showToast('Chat cleared', 'success');
    }
    
    exportChat() {
        if (this.messageHistory.length === 0) {
            window.AcadefyApp.showToast('No chat history to export', 'info');
            return;
        }
        
        const chatData = {
            sessionId: this.sessionId,
            exportDate: new Date().toISOString(),
            messageCount: this.messageCount,
            messages: this.messageHistory
        };
        
        const dataStr = JSON.stringify(chatData, null, 2);
        const filename = `acadefy-chat-${this.sessionId.substring(0, 8)}-${new Date().toISOString().split('T')[0]}.json`;
        
        window.AcadefyUtils.downloadAsFile(dataStr, filename);
        window.AcadefyApp.showToast('Chat exported successfully', 'success');
    }
    
    showErrorModal(errorMessage) {
        const modal = document.getElementById('error-modal');
        const messageElement = document.getElementById('error-message');
        
        if (modal && messageElement) {
            messageElement.textContent = errorMessage || 'An unexpected error occurred.';
            modal.style.display = 'flex';
        }
    }
    
    closeErrorModal() {
        const modal = document.getElementById('error-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
    
    handleChatFileUpload(event) {
        const files = Array.from(event.target.files);
        this.attachedFiles = files;
        this.displayAttachedFiles();
        
        // Auto-upload files and add to knowledge base
        this.uploadChatFiles(files);
    }
    
    async uploadChatFiles(files) {
        const attachedContainer = document.getElementById('chat-attached-files');
        
        try {
            for (const file of files) {
                // Show uploading status
                this.updateFileStatus(file.name, 'uploading');
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('title', file.name);
                
                const response = await fetch('/api/upload-direct', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    this.updateFileStatus(file.name, 'success');
                    
                    // Add a system message about the uploaded file
                    this.addMessage(`📎 Document uploaded: ${file.name}. You can now ask questions about its content!`, 'system');
                } else {
                    this.updateFileStatus(file.name, 'error');
                    window.AcadefyApp.showToast(`Failed to upload ${file.name}`, 'error');
                }
            }
        } catch (error) {
            console.error('Error uploading files:', error);
            window.AcadefyApp.showToast('Failed to upload files', 'error');
        }
    }
    
    displayAttachedFiles() {
        const container = document.getElementById('chat-attached-files');
        if (!container || !this.attachedFiles || this.attachedFiles.length === 0) {
            if (container) container.innerHTML = '';
            return;
        }
        
        container.innerHTML = `
            <div class="attached-files">
                ${this.attachedFiles.map(file => `
                    <div class="attached-file" data-filename="${file.name}">
                        <i class="fas fa-${this.getFileIcon(file.name)}"></i>
                        <span class="file-name">${file.name}</span>
                        <span class="file-status" id="status-${file.name}">📤</span>
                        <button class="remove-file" onclick="tutorInstance.removeAttachedFile('${file.name}')">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    updateFileStatus(filename, status) {
        const statusElement = document.getElementById(`status-${filename}`);
        if (statusElement) {
            const statusIcons = {
                'uploading': '⏳',
                'success': '✅',
                'error': '❌'
            };
            statusElement.textContent = statusIcons[status] || '📤';
        }
    }
    
    removeAttachedFile(filename) {
        if (this.attachedFiles) {
            this.attachedFiles = this.attachedFiles.filter(file => file.name !== filename);
            this.displayAttachedFiles();
        }
    }
    
    getFileIcon(filename) {
        const extension = filename.split('.').pop().toLowerCase();
        const iconMap = {
            'pdf': 'file-pdf',
            'docx': 'file-word',
            'pptx': 'file-powerpoint',
            'txt': 'file-alt'
        };
        return iconMap[extension] || 'file';
    }

    focusInput() {
        const messageInput = document.getElementById('message-input');
        if (messageInput) {
            setTimeout(() => messageInput.focus(), 100);
        }
    }
}

// Global functions for HTML onclick handlers
window.sendMessage = function() {
    if (window.tutorInstance) {
        window.tutorInstance.sendMessage();
    }
};

window.clearChat = function() {
    if (window.tutorInstance) {
        window.tutorInstance.clearChat();
    }
};

window.exportChat = function() {
    if (window.tutorInstance) {
        window.tutorInstance.exportChat();
    }
};

window.insertQuickMessage = function(message) {
    if (window.tutorInstance) {
        window.tutorInstance.insertQuickMessage(message);
    }
};

window.closeErrorModal = function() {
    if (window.tutorInstance) {
        window.tutorInstance.closeErrorModal();
    }
};

window.triggerFileUpload = function() {
    const fileInput = document.getElementById('chat-file-input');
    if (fileInput) {
        fileInput.click();
    }
};

// Initialize tutor when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.tutor-page')) {
        window.tutorInstance = new AcadefyTutor();
    }
});