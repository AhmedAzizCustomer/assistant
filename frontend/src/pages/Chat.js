import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chat.css';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchChatHistory = async () => {
    try {
      const response = await axios.get('/api/chat/history?limit=50');
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!inputMessage.trim()) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat/message', {
        content: inputMessage
      });

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.assistant_message.content,
        timestamp: response.data.assistant_message.timestamp
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = async () => {
    if (window.confirm('Are you sure you want to clear chat history?')) {
      try {
        await axios.delete('/api/chat/history');
        setMessages([]);
      } catch (error) {
        console.error('Error clearing history:', error);
      }
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <h1>AI Assistant Chat</h1>
        <button className="btn btn-secondary" onClick={clearHistory}>
          Clear History
        </button>
      </div>

      <div className="chat-container">
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <h2>Start a conversation!</h2>
              <p>Ask me anything about your tasks, schedule, meals, workouts, or anything else.</p>
              <div className="suggestions">
                <button onClick={() => setInputMessage("What's on my schedule today?")}>
                  What's on my schedule today?
                </button>
                <button onClick={() => setInputMessage("Show me my pending tasks")}>
                  Show me my pending tasks
                </button>
                <button onClick={() => setInputMessage("Help me plan my meals for the week")}>
                  Help me plan my meals for the week
                </button>
                <button onClick={() => setInputMessage("Suggest a workout for today")}>
                  Suggest a workout for today
                </button>
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-header">
                  <strong>{msg.role === 'user' ? 'You' : 'AI Assistant'}</strong>
                  <span className="timestamp">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="message assistant">
              <div className="message-header">
                <strong>AI Assistant</strong>
              </div>
              <div className="message-content typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-input-form" onSubmit={sendMessage}>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isLoading || !inputMessage.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chat;
