import React from 'react';

function Email() {
  return (
    <div>
      <h1>Email Management</h1>
      <div className="card">
        <h2>Connect Email Accounts</h2>
        <p>Connect your Gmail and Outlook accounts to manage emails with AI assistance.</p>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button className="btn btn-primary">Connect Gmail</button>
          <button className="btn btn-primary">Connect Outlook</button>
        </div>
      </div>
      <div className="card">
        <h2>Email Features</h2>
        <ul>
          <li>Smart email categorization and prioritization</li>
          <li>AI-powered email summaries</li>
          <li>Draft responses with AI assistance</li>
          <li>Automatic inbox organization</li>
        </ul>
      </div>
    </div>
  );
}

export default Email;
