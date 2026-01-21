'use client';
import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../lib/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useRouter } from 'next/navigation';

export default function Chat() {
  const { user, logout, loading } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
        router.push('/login');
    }
  }, [user, loading, router]);

  useEffect(() => {
      if (user) {
          fetchMessages();
      }
  }, [user]);

  const fetchMessages = async () => {
      try {
          const res = await api.get('chat/');
          setMessages(res.data);
          scrollToBottom();
      } catch (error) {
          console.error("Error fetching messages", error);
      }
  };

  const clearSession = async () => {
      try {
          await api.post('chat/clear/', {});
          setMessages([]);
      } catch (error) {
          console.error("Error clearing session", error);
      }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (!loading && user && inputRef.current) {
        inputRef.current.focus();
    }
  }, [loading, user]);

  const handleInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = e.target.scrollHeight + 'px';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const tempMessage = { message: input, response: null, id: 'temp-' + Date.now() };
    setMessages(prev => [...prev, tempMessage]);
    setInput('');
    if (inputRef.current) {
        inputRef.current.style.height = 'auto';
    }
    setIsTyping(true);

    try {
        const res = await api.post('chat/', { message: input }); // API call
        // Replace temp message with actual response
        setMessages(prev => prev.map(msg => msg.id === tempMessage.id ? res.data : msg));
    } catch (error) {
        console.error("Error sending message", error);
        setMessages(prev => prev.filter(msg => msg.id !== tempMessage.id)); // Remove failed message
    } finally {
        setIsTyping(false);
    }
  };

  if (loading) return <div style={{display:'flex', justifyContent:'center', alignItems:'center', height:'100vh', color: '#fff'}}>Loading...</div>;
  if (!user) return null;

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-title">💬 Chat</div>
        <div className="auth-section">
          <span className="welcome-text" style={{marginRight: '10px'}}>Welcome, {user.username || 'User'}</span>
          <div className="auth-buttons">
            <button onClick={clearSession} style={{marginRight: '8px'}}>Clear Chat</button>
            <button onClick={logout} className="logout-btn">Logout</button>
          </div>
        </div>
      </div>

      <div className="messages-box">
        <ul className="messages-list">
          <li className="message received">
            <div className="message-content">
              <div className="message-sender">AI Chatbot</div>
              Hi {user.username || 'there'}, I am your AI Chatbot. You can ask me anything.
            </div>
          </li>

          {messages.map((chat, index) => (
            <div key={chat.id || index}>
                <li className="message sent">
                    <div className="message-content">{chat.message}</div>
                </li>
                {chat.response && (
                    <li className="message received">
                        <div className="message-content">
                        <div className="message-sender">AI Chatbot</div>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{chat.response}</ReactMarkdown>
                        </div>
                    </li>
                )}
            </div>
          ))}

          {isTyping && (
            <li className="typing-indicator">
                <div className="typing-dots">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                </div>
            </li>
          )}
          <div ref={messagesEndRef} />
        </ul>
      </div>

      <form className="message-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            ref={inputRef}
            className="message-input"
            placeholder="Type a message..."
            rows="1"
            value={input}
            onChange={handleInput}
            onKeyDown={(e) => {
                if(e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                }
            }}
          ></textarea>
          <button type="submit" className="btn-send" disabled={!input.trim()}>
            <svg
              className="send-icon"
              width="18"
              height="18"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
}
