import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import SummaryCards from './components/SummaryCards';
import EventFeed from './components/EventFeed';
import CommandTable from './components/CommandTable';
import AttackChart from './components/AttackChart';
import GeoTable from './components/GeoTable';
import Login from './components/Login';
import './App.css';

const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [token, setToken] = useState(sessionStorage.getItem('token'));
  const [summary, setSummary] = useState(null);
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const logout = useCallback(() => {
    sessionStorage.removeItem('token');
    setToken(null);
  }, []);

  const fetchData = useCallback(async () => {
    const headers = { Authorization: `Bearer ${token}` };
    try {
      const [s, e] = await Promise.all([
        axios.get(`${API_URL}/api/summary`, { headers }),
        axios.get(`${API_URL}/api/events`, { headers }),
      ]);
      setSummary(s.data);
      setEvents(e.data.events);
      setLastUpdated(new Date().toLocaleTimeString());
      setError(null);
    } catch (err) {
      if (err.response && err.response.status === 401) logout();
      else setError('Cannot connect to honeypot API. Make sure Flask is running.');
    }
  }, [token, logout]);

  useEffect(() => {
    if (!token) return;
    fetchData();
    const id = setInterval(fetchData, 5000);
    return () => clearInterval(id);
  }, [token, fetchData]);

  const handleLogin = (t) => {
    sessionStorage.setItem('token', t);
    setToken(t);
  };

  if (!token) return <Login apiUrl={API_URL} onLogin={handleLogin} />;
  if (error) return <div className="error"><h2>{error}</h2></div>;
  if (!summary) return <div className="loading"><h2>Connecting to Honeypot...</h2></div>;

  return (
    <div className="app">
      <header className="header">
        <h1>Real-Time Cyber Threat Intelligence Dashboard</h1>
        <p>Mount Kenya University — Honeypot Monitoring System</p>
        <span className="last-updated">Last updated: {lastUpdated}</span>
        <button onClick={logout} style={{ marginLeft: 12 }}>Sign out</button>
      </header>
      <main className="main">
        <SummaryCards summary={summary} />
        <AttackChart events={events} />
        <GeoTable events={events} />
        <div className="bottom-grid">
          <EventFeed events={events} />
          <CommandTable events={events} />
        </div>
      </main>
    </div>
  );
}

export default App;
