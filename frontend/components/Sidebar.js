import React, { useState, useEffect } from 'react';
import { saveAPIKey, getAPIKeyStatus, deleteAPIKey, getAvailableModels } from '../lib/api';
import ModelSelector from './ModelSelector';

export default function Sidebar({ isOpen, onClose }) {
  const [apiKey, setApiKey] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('llama-3.3-70b-versatile');

  useEffect(() => {
    fetchStatus();
  }, []);

  useEffect(() => {
      if (isSaved) {
          fetchModels();
      }
  }, [isSaved]);

  const fetchStatus = async () => {
    try {
      const res = await getAPIKeyStatus();
      if (res.data && res.data.selected_model) {
        setIsSaved(true);
        setSelectedModel(res.data.selected_model);
      } else {
        setIsSaved(false);
      }
    } catch (error) {
      console.error("Error fetching status", error);
      setIsSaved(false);
    }
  };

  const fetchModels = async () => {
      try {
          const res = await getAvailableModels();
          setModels(res.data);
      } catch (error) {
          console.error("Error fetching models", error);
      }
  };

  const handleSave = async () => {
    setIsLoading(true);
    setStatusMessage('');
    try {
      const payloadKey = apiKey.trim() ? apiKey.trim() : undefined;

      if (!isSaved && !payloadKey) {
          setStatusMessage('Please enter an API Key.');
          setIsLoading(false);
          return;
      }

      await saveAPIKey(payloadKey, selectedModel);
      setIsSaved(true);
      setStatusMessage('Settings saved successfully!');
      setApiKey(''); // Clear input for security
      fetchModels(); // Refresh models
    } catch (error) {
      console.error("Error saving settings", error);
      setStatusMessage('Error saving settings.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to remove your API Key?")) return;
    setIsLoading(true);
    try {
      await deleteAPIKey();
      setIsSaved(false);
      setModels([]);
      setApiKey('');
      setSelectedModel('llama-3.3-70b-versatile');
      setStatusMessage('API Key removed.');
    } catch (error) {
      console.error("Error deleting key", error);
      setStatusMessage('Error removing key.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <button className="close-btn" onClick={onClose}>&times;</button>
      <div className="sidebar-content">
        <h2>Settings</h2>

        <div className="form-group">
          <label>Groq API Key</label>
          {isSaved ? (
            <div className="key-status">
              <span className="status-badge success">Key Saved</span>
              <button className="btn-text" onClick={handleDelete}>Remove</button>
            </div>
          ) : (
             <span className="status-badge warning">Not Configured</span>
          )}
          <input
            type="password"
            placeholder={isSaved ? "Enter new key to update" : "Enter your Groq API Key"}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="input-field"
          />
        </div>

        <ModelSelector
            models={models}
            selectedModel={selectedModel}
            onSelect={setSelectedModel}
            disabled={!isSaved && models.length === 0}
        />

        <button
            onClick={handleSave}
            className="btn-primary"
            disabled={isLoading}
        >
          {isLoading ? 'Saving...' : 'Save Settings'}
        </button>

        {statusMessage && <p className="status-message">{statusMessage}</p>}
      </div>
    </div>
  );
}
