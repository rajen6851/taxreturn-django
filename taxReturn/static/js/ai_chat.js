// static/js/ai_chat.js
class AIChat {
    constructor(config) {
        this.endpoint = config.endpoint;
        this.sessionId = config.sessionId || this.generateSessionId();
        this.userContext = config.userContext || {};
        this.messages = [];
        this.isProcessing = false;
    }
    
    init() {
        this.bindEvents();
        this.showWelcomeMessage();
    }
    
    bindEvents() {
        // Send button click
        document.getElementById('sendButton').addEventListener('click', () => this.sendMessage());
        
        // Enter key in input
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Voice input
        document.getElementById('voiceButton').addEventListener('click', () => this.startVoiceInput());
        
        // Document upload
        document.getElementById('uploadButton').addEventListener('change', (e) => this.uploadDocument(e));
    }
    
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message || this.isProcessing) return;
        
        // Clear input
        input.value = '';
        
        // Add user message
        this.addMessage('user', message);
        
        // Show typing indicator
        this.showTyping();
        
        try {
            this.isProcessing = true;
            
            // Call Django API
            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    context: this.userContext
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTyping();
            
            if (data.status === 'success') {
                // Add AI response
                this.addMessage('ai', data.response, {
                    intent: data.intent,
                    confidence: data.confidence,
                    sources: data.sources,
                    suggestions: data.suggestions
                });
                
                // Update suggestions
                this.updateSuggestions(data.suggestions);
                
                // Update context if needed
                this.updateUserContext(data);
                
            } else {
                this.addMessage('ai', `Error: ${data.error || 'Unknown error'}`);
            }
            
        } catch (error) {
            this.removeTyping();
            this.addMessage('ai', 'Sorry, I am having trouble connecting. Please try again.');
            console.error('Chat error:', error);
        } finally {
            this.isProcessing = false;
        }
    }
    
    addMessage(type, content, metadata = {}) {
        const message = {
            type,
            content,
            timestamp: new Date().toISOString(),
            metadata
        };
        
        this.messages.push(message);
        this.renderMessage(message);
        
        // Scroll to bottom
        this.scrollToBottom();
        
        // Save to localStorage
        this.saveToLocalStorage();
    }
    
    renderMessage(message) {
        const template = document.getElementById('messageTemplate');
        const clone = document.importNode(template.content, true);
        
        const messageDiv = clone.querySelector('.message');
        messageDiv.dataset.type = message.type;
        
        // Set avatar
        const avatar = messageDiv.querySelector('.avatar');
        avatar.innerHTML = message.type === 'user' 
            ? '<i class="fas fa-user"></i>' 
            : '<i class="fas fa-robot"></i>';
        
        // Set content
        const contentDiv = messageDiv.querySelector('.text');
        contentDiv.innerHTML = this.formatContent(message.content, message.metadata);
        
        // Set time
        const timeDiv = messageDiv.querySelector('.time');
        timeDiv.textContent = new Date(message.timestamp).toLocaleTimeString();
        
        // Add sources if available
        if (message.metadata.sources && message.metadata.sources.length > 0) {
            const sourcesDiv = messageDiv.querySelector('.sources');
            sourcesDiv.innerHTML = this.formatSources(message.metadata.sources);
        }
        
        // Add to chat container
        document.getElementById('chatMessages').appendChild(clone);
    }
    
    formatContent(content, metadata) {
        let formatted = content;
        
        // Add confidence badge
        if (metadata.confidence) {
            const confidenceColor = metadata.confidence > 0.8 ? 'success' 
                                 : metadata.confidence > 0.6 ? 'warning' 
                                 : 'danger';
            
            formatted += `<div class="confidence-badge badge-${confidenceColor}">
                Confidence: ${(metadata.confidence * 100).toFixed(0)}%
            </div>`;
        }
        
        // Add intent badge
        if (metadata.intent && metadata.intent !== 'other') {
            formatted += `<div class="intent-badge">${metadata.intent}</div>`;
        }
        
        return formatted;
    }
    
    formatSources(sources) {
        let html = '<div class="sources-container"><strong>Sources:</strong><ul>';
        
        sources.forEach(source => {
            html += `<li>
                <div class="source-content">${source.content}</div>
                <div class="source-meta">${source.metadata.source || 'Unknown'}</div>
            </li>`;
        });
        
        html += '</ul></div>';
        return html;
    }
    
    updateSuggestions(suggestions) {
        const container = document.querySelector('.quick-suggestions');
        if (!container || !suggestions) return;
        
        container.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const button = document.createElement('button');
            button.className = 'quick-suggestion';
            button.textContent = suggestion;
            button.addEventListener('click', () => {
                document.getElementById('chatInput').value = suggestion;
                this.sendMessage();
            });
            
            container.appendChild(button);
        });
    }
    
    showTyping() {
        // Add typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message typing';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="avatar"><i class="fas fa-robot"></i></div>
            <div class="content">
                <div class="text">
                    <div class="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('chatMessages').appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    removeTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }
    
    scrollToBottom() {
        const container = document.getElementById('chatMessages');
        container.scrollTop = container.scrollHeight;
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    getCSRFToken() {
        // Get CSRF token from cookie
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    saveToLocalStorage() {
        // Save chat history to localStorage
        localStorage.setItem(`chat_${this.sessionId}`, JSON.stringify(this.messages));
    }
    
    loadFromLocalStorage() {
        // Load chat history from localStorage
        const saved = localStorage.getItem(`chat_${this.sessionId}`);
        if (saved) {
            this.messages = JSON.parse(saved);
            this.messages.forEach(msg => this.renderMessage(msg));
        }
    }
    
    async uploadDocument(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('document', file);
        formData.append('type', this.detectDocumentType(file.name));
        
        try {
            const response = await fetch('/api/analyze-document/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.addMessage('system', `Document analyzed: ${file.name}`);
                // Update context with document data
                this.userContext.documentAnalysis = data.analysis;
            }
            
        } catch (error) {
            console.error('Document upload error:', error);
        }
    }
    
    detectDocumentType(filename) {
        if (filename.includes('Form16')) return 'form16';
        if (filename.includes('Bank')) return 'bank_statement';
        if (filename.includes('Invoice')) return 'invoice';
        if (filename.includes('PAN')) return 'pan_card';
        return 'auto';
    }
}