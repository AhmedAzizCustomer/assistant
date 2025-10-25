import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Settings.css';

function Settings() {
  const [systemStatus, setSystemStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const [formData, setFormData] = useState({
    // AI Settings
    anthropic_api_key: '',
    openai_api_key: '',
    default_ai_provider: 'anthropic',
    claude_model: 'claude-3-5-sonnet-20241022',
    openai_model: 'gpt-4-turbo-preview',

    // Email Settings
    gmail_client_id: '',
    gmail_client_secret: '',
    outlook_client_id: '',
    outlook_client_secret: '',

    // Calendar Settings
    google_calendar_client_id: '',
    google_calendar_client_secret: '',

    // Database
    database_url: 'sqlite:///./assistant.db',

    // App Settings
    environment: 'production',
    secret_key: ''
  });

  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const response = await axios.get('/api/settings/status');
      setSystemStatus(response.data);
    } catch (error) {
      console.error('Error checking system status:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setSuccessMessage('');

    try {
      // Filter out empty values
      const settingsToSave = {};
      Object.entries(formData).forEach(([key, value]) => {
        if (value && value.trim() !== '') {
          settingsToSave[key] = value;
        }
      });

      await axios.post('/api/settings/bulk', {
        settings: settingsToSave
      });

      setSuccessMessage('Settings saved successfully!');
      await checkSystemStatus();

      // Clear form after successful save
      setTimeout(() => {
        setSuccessMessage('');
      }, 5000);

    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Error saving settings. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const testAIConnection = async () => {
    setIsTesting(true);
    setTestResult(null);

    try {
      const response = await axios.post('/api/settings/test-ai');
      setTestResult(response.data);
    } catch (error) {
      setTestResult({
        success: false,
        message: 'Failed to test connection'
      });
    } finally {
      setIsTesting(false);
    }
  };

  const generateSecretKey = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let key = '';
    for (let i = 0; i < 50; i++) {
      key += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setFormData(prev => ({ ...prev, secret_key: key }));
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>System Settings</h1>
        {systemStatus && (
          <div className={`status-badge ${systemStatus.is_configured ? 'configured' : 'not-configured'}`}>
            {systemStatus.is_configured ? '✓ Configured' : '⚠ Not Configured'}
          </div>
        )}
      </div>

      {successMessage && (
        <div className="success-message">
          {successMessage}
        </div>
      )}

      {systemStatus && !systemStatus.is_configured && (
        <div className="alert alert-info">
          <h3>Welcome to AI Personal Assistant!</h3>
          <p>Please configure your API keys below to get started. At minimum, you need either an Anthropic or OpenAI API key.</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="settings-form">
        {/* AI Configuration */}
        <div className="settings-section">
          <h2>🤖 AI Configuration</h2>
          <p className="section-description">
            Configure your AI providers. You need at least one API key (Anthropic or OpenAI).
          </p>

          <div className="form-group">
            <label htmlFor="anthropic_api_key">
              Anthropic API Key
              <span className="help-text">Get from <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer">console.anthropic.com</a></span>
            </label>
            <input
              type="password"
              id="anthropic_api_key"
              name="anthropic_api_key"
              value={formData.anthropic_api_key}
              onChange={handleInputChange}
              placeholder="sk-ant-api-..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="openai_api_key">
              OpenAI API Key
              <span className="help-text">Get from <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer">platform.openai.com</a></span>
            </label>
            <input
              type="password"
              id="openai_api_key"
              name="openai_api_key"
              value={formData.openai_api_key}
              onChange={handleInputChange}
              placeholder="sk-..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="default_ai_provider">Default AI Provider</label>
            <select
              id="default_ai_provider"
              name="default_ai_provider"
              value={formData.default_ai_provider}
              onChange={handleInputChange}
            >
              <option value="anthropic">Anthropic Claude</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="claude_model">Claude Model</label>
              <input
                type="text"
                id="claude_model"
                name="claude_model"
                value={formData.claude_model}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="openai_model">OpenAI Model</label>
              <input
                type="text"
                id="openai_model"
                name="openai_model"
                value={formData.openai_model}
                onChange={handleInputChange}
              />
            </div>
          </div>

          {systemStatus && systemStatus.has_ai_keys && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={testAIConnection}
              disabled={isTesting}
            >
              {isTesting ? 'Testing...' : 'Test AI Connection'}
            </button>
          )}

          {testResult && (
            <div className={`test-result ${testResult.success ? 'success' : 'error'}`}>
              <strong>{testResult.success ? '✓ Success!' : '✗ Failed'}</strong>
              <p>{testResult.message}</p>
              {testResult.response && <p>Response: {testResult.response}</p>}
            </div>
          )}
        </div>

        {/* Email Configuration */}
        <div className="settings-section">
          <h2>📧 Email Configuration (Optional)</h2>
          <p className="section-description">
            Configure email providers for email management features.
          </p>

          <h3>Gmail</h3>
          <div className="form-group">
            <label htmlFor="gmail_client_id">Gmail Client ID</label>
            <input
              type="text"
              id="gmail_client_id"
              name="gmail_client_id"
              value={formData.gmail_client_id}
              onChange={handleInputChange}
              placeholder="xxxxx.apps.googleusercontent.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="gmail_client_secret">Gmail Client Secret</label>
            <input
              type="password"
              id="gmail_client_secret"
              name="gmail_client_secret"
              value={formData.gmail_client_secret}
              onChange={handleInputChange}
            />
          </div>

          <h3>Outlook</h3>
          <div className="form-group">
            <label htmlFor="outlook_client_id">Outlook Client ID</label>
            <input
              type="text"
              id="outlook_client_id"
              name="outlook_client_id"
              value={formData.outlook_client_id}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="outlook_client_secret">Outlook Client Secret</label>
            <input
              type="password"
              id="outlook_client_secret"
              name="outlook_client_secret"
              value={formData.outlook_client_secret}
              onChange={handleInputChange}
            />
          </div>
        </div>

        {/* Calendar Configuration */}
        <div className="settings-section">
          <h2>📅 Calendar Configuration (Optional)</h2>
          <p className="section-description">
            Configure calendar providers. Can use same Google OAuth credentials as Gmail.
          </p>

          <div className="form-group">
            <label htmlFor="google_calendar_client_id">Google Calendar Client ID</label>
            <input
              type="text"
              id="google_calendar_client_id"
              name="google_calendar_client_id"
              value={formData.google_calendar_client_id}
              onChange={handleInputChange}
              placeholder="Same as Gmail or separate"
            />
          </div>

          <div className="form-group">
            <label htmlFor="google_calendar_client_secret">Google Calendar Client Secret</label>
            <input
              type="password"
              id="google_calendar_client_secret"
              name="google_calendar_client_secret"
              value={formData.google_calendar_client_secret}
              onChange={handleInputChange}
            />
          </div>
        </div>

        {/* Advanced Settings */}
        <div className="settings-section">
          <h2>⚙️ Advanced Settings</h2>

          <div className="form-group">
            <label htmlFor="database_url">
              Database URL
              <span className="help-text">Default: SQLite (recommended for single user)</span>
            </label>
            <input
              type="text"
              id="database_url"
              name="database_url"
              value={formData.database_url}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="secret_key">
              Secret Key
              <span className="help-text">Used for encryption</span>
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="password"
                id="secret_key"
                name="secret_key"
                value={formData.secret_key}
                onChange={handleInputChange}
                placeholder="Generate or enter a random key"
                style={{ flex: 1 }}
              />
              <button
                type="button"
                className="btn btn-secondary"
                onClick={generateSecretKey}
              >
                Generate
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="environment">Environment</label>
            <select
              id="environment"
              name="environment"
              value={formData.environment}
              onChange={handleInputChange}
            >
              <option value="development">Development</option>
              <option value="production">Production</option>
            </select>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary btn-large"
            disabled={isLoading}
          >
            {isLoading ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </form>

      <div className="settings-help">
        <h3>Need Help?</h3>
        <ul>
          <li><strong>Anthropic API Key:</strong> Sign up at <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer">console.anthropic.com</a></li>
          <li><strong>OpenAI API Key:</strong> Sign up at <a href="https://platform.openai.com/" target="_blank" rel="noopener noreferrer">platform.openai.com</a></li>
          <li><strong>Gmail/Google Calendar:</strong> Create OAuth credentials at <a href="https://console.cloud.google.com/" target="_blank" rel="noopener noreferrer">Google Cloud Console</a></li>
          <li><strong>Outlook:</strong> Register app at <a href="https://portal.azure.com/" target="_blank" rel="noopener noreferrer">Azure Portal</a></li>
        </ul>
      </div>
    </div>
  );
}

export default Settings;
