import React, { useState } from 'react';
import axios from 'axios';

function Login({ apiUrl, onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${apiUrl}/api/login`, { username, password });
      onLogin(res.data.token);
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="loading">
      <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 12, width: 300 }}>
        <h2>Administrator login</h2>
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit">Sign in</button>
        {error && <span style={{ color: '#EF4444' }}>{error}</span>}
      </form>
    </div>
  );
}

export default Login;
