"""
Simple Chat Processor
"""
import json
import time

class ChatProcessor:
    """Simple chat processor for storing and managing conversations"""
    
    def __init__(self):
        self.sessions = {}
        print("✅ ChatProcessor initialized")
    
    def create_session(self, user_id=None):
        """Create a new chat session"""
        import uuid
        session_id = str(uuid.uuid4())[:8]
        self.sessions[session_id] = {
            'created_at': time.time(),
            'messages': [],
            'user_id': user_id
        }
        return session_id
    
    def save_message(self, session_id, user_message, ai_response, intent=None):
        """Save a message to chat history"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': time.time(),
                'messages': []
            }
        
        message = {
            'timestamp': time.time(),
            'user': user_message,
            'ai': ai_response,
            'intent': intent
        }
        
        self.sessions[session_id]['messages'].append(message)
        
        # Keep only last 50 messages
        if len(self.sessions[session_id]['messages']) > 50:
            self.sessions[session_id]['messages'] = self.sessions[session_id]['messages'][-50:]
        
        return True
    
    def get_session_history(self, session_id, limit=20):
        """Get chat history for a session"""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]['messages']
        return messages[-limit:] if limit else messages
    
    def clear_session(self, session_id):
        """Clear a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False