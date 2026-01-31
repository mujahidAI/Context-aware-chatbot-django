'use client';
import { useState, useEffect }from 'react';
import api from '../lib/api';

/**
 * Sidebar component for managing Groq API key and model selection.
 * Allows users to:
 * - Enter and save their own Groq API key
 * - View available models based on their API key
 * - Select which model to use for chat
 */
export default function Sidebar({ isOpen, onClose, onModelChange }) {
    const [apiKey, setApiKey] = useState('');
    const [hasKey, setHasKey] = useState(false);
    const [keyPreview, setKeyPreview] = useState(null);
    const [selectedModel, setSelectedModel] = useState('llama-3.3-70b-versatile');
    const [models, setModels] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });
    const [showApiKey, setShowApiKey] = useState(false);

    // Fetch user's API key status on mount
    useEffect(() => {
        if (isOpen) {
            fetchKeyStatus();
        }
    }, [isOpen]);

    // Fetch available models when user has a key
    useEffect(() => {
        if (hasKey) {
            fetchModels();
        }
    }, [hasKey]);

    const fetchKeyStatus = async () => {
        try {
            const res = await api.get('user-api-key/');
            setHasKey(res.data.has_key || false);
            setKeyPreview(res.data.key_preview || null);
            setSelectedModel(res.data.selected_model || 'llama-3.3-70b-versatile');
        } catch (error) {
            console.error('Error fetching API key status:', error);
        }
    };

    const fetchModels = async () => {
        try {
            const res = await api.get('available-models/');
            setModels(res.data.models || []);
            if (res.data.selected_model) {
                setSelectedModel(res.data.selected_model);
            }
        } catch (error) {
            console.error('Error fetching models:', error);
            if (error.response?.data?.error) {
                setMessage({ type: 'error', text: error.response.data.error });
            }
        }
    };

    const handleSaveKey = async (e) => {
        e.preventDefault();
        if (!apiKey.trim()) {
            setMessage({ type: 'error', text: 'Please enter an API key' });
            return;
        }

        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const res = await api.post('user-api-key/', { 
                api_key: apiKey,
                selected_model: selectedModel 
            });
            setHasKey(true);
            setKeyPreview(res.data.key_preview);
            setApiKey(''); // Clear input after saving
            setMessage({ type: 'success', text: 'API key saved successfully!' });
            await fetchModels(); // Refresh available models
        } catch (error) {
            const errorMsg = error.response?.data?.api_key?.[0] || 
                           error.response?.data?.error || 
                           'Failed to save API key';
            setMessage({ type: 'error', text: errorMsg });
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteKey = async () => {
        if (!confirm('Are you sure you want to remove your API key?')) return;

        setLoading(true);
        try {
            await api.delete('user-api-key/');
            setHasKey(false);
            setKeyPreview(null);
            setModels([]);
            setMessage({ type: 'success', text: 'API key removed' });
        } catch (error) {
            setMessage({ type: 'error', text: 'Failed to remove API key' });
        } finally {
            setLoading(false);
        }
    };

    const handleModelChange = async (modelId) => {
        setSelectedModel(modelId);
        try {
            await api.post('select-model/', { selected_model: modelId });
            setMessage({ type: 'success', text: `Model changed to ${modelId}` });
            if (onModelChange) onModelChange(modelId);
        } catch (error) {
            setMessage({ type: 'error', text: 'Failed to update model' });
        }
    };

    // Clear message after 3 seconds
    useEffect(() => {
        if (message.text) {
            const timer = setTimeout(() => setMessage({ type: '', text: '' }), 3000);
            return () => clearTimeout(timer);
        }
    }, [message]);

    return (
        <>
            {/* Overlay */}
            <div 
                className={`sidebar-overlay ${isOpen ? 'active' : ''}`}
                onClick={onClose}
            />
            
            {/* Sidebar */}
            <div className={`sidebar ${isOpen ? 'open' : ''}`}>
                <div className="sidebar-header">
                    <h2>⚙️ Settings</h2>
                    <button className="sidebar-close" onClick={onClose}>×</button>
                </div>

                <div className="sidebar-content">
                    {/* Message Display */}
                    {message.text && (
                        <div className={`sidebar-message ${message.type}`}>
                            {message.text}
                        </div>
                    )}

                    {/* API Key Section */}
                    <div className="sidebar-section">
                        <h3>🔑 Groq API Key</h3>
                        <p className="sidebar-description">
                            Enter your own Groq API key to use the chatbot. 
                            <a href="https://console.groq.com/keys" target="_blank" rel="noopener noreferrer">
                                Get your free key →
                            </a>
                        </p>

                        {hasKey ? (
                            <div className="key-status">
                                <div className="key-preview">
                                    <span className="key-label">Current Key:</span>
                                    <span className="key-value">{keyPreview}</span>
                                </div>
                                <div className="key-actions">
                                    <button 
                                        className="btn-update-key"
                                        onClick={() => setHasKey(false)}
                                    >
                                        Update Key
                                    </button>
                                    <button 
                                        className="btn-delete-key"
                                        onClick={handleDeleteKey}
                                        disabled={loading}
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <form onSubmit={handleSaveKey} className="api-key-form">
                                <div className="input-wrapper">
                                    <input
                                        type={showApiKey ? 'text' : 'password'}
                                        value={apiKey}
                                        onChange={(e) => setApiKey(e.target.value)}
                                        placeholder="gsk_..."
                                        className="api-key-input"
                                    />
                                    <button 
                                        type="button"
                                        className="toggle-visibility"
                                        onClick={() => setShowApiKey(!showApiKey)}
                                    >
                                        {showApiKey ? '👁️' : '👁️‍🗨️'}
                                    </button>
                                </div>
                                <button 
                                    type="submit" 
                                    className="btn-save-key"
                                    disabled={loading || !apiKey.trim()}
                                >
                                    {loading ? 'Validating...' : 'Save API Key'}
                                </button>
                            </form>
                        )}
                    </div>

                    {/* Model Selection Section */}
                    <div className="sidebar-section">
                        <h3>🤖 Model Selection</h3>
                        <p className="sidebar-description">
                            Choose which AI model to use for your conversations.
                        </p>

                        {hasKey && models.length > 0 ? (
                            <div className="model-list">
                                {models.map((model) => (
                                    <div 
                                        key={model.id}
                                        className={`model-item ${selectedModel === model.id ? 'selected' : ''}`}
                                        onClick={() => handleModelChange(model.id)}
                                    >
                                        <div className="model-info">
                                            <span className="model-name">{model.id}</span>
                                            <span className="model-context">
                                                {(model.context_window / 1000).toFixed(0)}K context
                                            </span>
                                        </div>
                                        {selectedModel === model.id && (
                                            <span className="model-check">✓</span>
                                        )}
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="no-models">
                                {hasKey ? (
                                    <p>Loading models...</p>
                                ) : (
                                    <p>Add your API key to see available models</p>
                                )}
                            </div>
                        )}
                    </div>

                    {/* Info Section */}
                    <div className="sidebar-section sidebar-info">
                        <h3>ℹ️ About</h3>
                        <p>
                            Your API key is encrypted and stored securely. 
                            It will only be used to make requests to Groq on your behalf.
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
}
