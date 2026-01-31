import React from 'react';

export default function ModelSelector({ models, selectedModel, onSelect, disabled }) {
  return (
    <div className="model-selector">
      <label htmlFor="model-select" className="model-label">Select Model</label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={(e) => onSelect(e.target.value)}
        disabled={disabled || models.length === 0}
        className="model-dropdown"
      >
        {models.length === 0 ? (
          <option value="" disabled>No models available (Save API Key first)</option>
        ) : (
          models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name} ({model.context_window})
            </option>
          ))
        )}
      </select>
    </div>
  );
}
