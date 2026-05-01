import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface QRCode {
  id: number;
  short_token: string;
  original_url: string;
  created_at: string;
  updated_at?: string;
  deleted_at?: string;
  expires_at?: string;
}

const API_BASE = 'http://localhost:8000';

function App() {
  const [qrCodes, setQrCodes] = useState<QRCode[]>([]);
  const [url, setUrl] = useState('');
  const [expiresAt, setExpiresAt] = useState('');
  const [editing, setEditing] = useState<string | null>(null);
  const [editUrl, setEditUrl] = useState('');
  const [editExpiresAt, setEditExpiresAt] = useState('');
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    fetchQrCodes();
  }, []);

  const fetchQrCodes = async () => {
    try {
      const response = await axios.get(`${API_BASE}/qr`);
      setQrCodes(response.data);
    } catch (error) {
      console.error('Error fetching QR codes:', error);
    }
  };

  const createQrCode = async () => {
    try {
      const data: any = { original_url: url };
      if (expiresAt) data.expires_at = new Date(expiresAt).toISOString();
      await axios.post(`${API_BASE}/qr`, data);
      await fetchQrCodes();
      setUrl('');
      setExpiresAt('');
      setMessage('QR code created successfully.');
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Error creating QR code.');
      console.error('Error creating QR code:', error);
    }
  };

  const updateQrCode = async (token: string) => {
    try {
      const data: any = {};
      if (editUrl) data.original_url = editUrl;
      if (editExpiresAt) data.expires_at = new Date(editExpiresAt).toISOString();
      await axios.put(`${API_BASE}/qr/${encodeURIComponent(token)}`, data);
      await fetchQrCodes();
      setEditing(null);
      setEditUrl('');
      setEditExpiresAt('');
      setMessage('QR code updated successfully.');
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Error updating QR code.');
      console.error('Error updating QR code:', error);
    }
  };

  const deleteQrCode = async (token: string) => {
    try {
      await axios.delete(`${API_BASE}/qr/${encodeURIComponent(token)}`);
      await fetchQrCodes();
      setMessage('QR code deleted successfully.');
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Error deleting QR code.');
      console.error('Error deleting QR code:', error);
    }
  };

  const startEdit = (qr: QRCode) => {
    setEditing(qr.short_token);
    setEditUrl(qr.original_url);
    setEditExpiresAt(qr.expires_at || '');
  };

  const copyLink = async (link: string) => {
    try {
      await navigator.clipboard.writeText(link);
      setMessage('Short URL copied to clipboard.');
    } catch {
      setMessage('Copy failed.');
    }
  };

  return (
    <div className="App">
      <h1>QR Code Generator</h1>
      <div className="create-form">
        <input
          type="url"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <div className="date-field">
          <label htmlFor="expiresAt">Set an expiration date (optional)</label>
          <input
            id="expiresAt"
            type="datetime-local"
            value={expiresAt}
            onChange={(e) => setExpiresAt(e.target.value)}
          />
        </div>
        <button onClick={createQrCode}>Create QR Code</button>
      </div>
      {message && <div className="message">{message}</div>}
      <div className="qr-list">
        {qrCodes.map((qr) => (
          <div key={qr.id} className="qr-item">
            <div className="qr-header">
              <div>
                <p className="qr-label">Token</p>
                <p className="qr-value">{qr.short_token}</p>
              </div>
              <div>
                <p className="qr-label">Short URL</p>
                <p className="qr-value short-url">{`${API_BASE}/qr/${encodeURIComponent(qr.short_token)}`}</p>
                <button className="small-button" onClick={() => copyLink(`${API_BASE}/qr/${encodeURIComponent(qr.short_token)}`)}>
                  Copy link
                </button>
              </div>
            </div>
            <p className="qr-label">Original URL</p>
            <p className="qr-value">{qr.original_url}</p>
            <p className="qr-label">Created</p>
            <p className="qr-value">{new Date(qr.created_at).toLocaleString()}</p>
            {qr.expires_at && (
              <>
                <p className="qr-label">Expires</p>
                <p className="qr-value">{new Date(qr.expires_at).toLocaleString()}</p>
              </>
            )}
            <img className="qr-image" src={`${API_BASE}/qr/${encodeURIComponent(qr.short_token)}/image`} alt="QR Code" />
            {editing === qr.short_token ? (
              <div>
                <input
                  type="url"
                  value={editUrl}
                  onChange={(e) => setEditUrl(e.target.value)}
                />
                <input
                  type="datetime-local"
                  value={editExpiresAt}
                  onChange={(e) => setEditExpiresAt(e.target.value)}
                />
                <button onClick={() => updateQrCode(qr.short_token)}>Save</button>
                <button onClick={() => setEditing(null)}>Cancel</button>
              </div>
            ) : (
              <div>
                <button onClick={() => startEdit(qr)}>Edit</button>
                <button onClick={() => deleteQrCode(qr.short_token)}>Delete</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;