import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import SummaryCards from './components/SummaryCards';
import EventFeed from './components/EventFeed';
import CommandTable from './components/CommandTable';
import AttackChart from './components/AttackChart';
import GeoTable from './components/GeoTable';
import Login from './components/Login';
import './App.css';

const API_URL = 'http://127.0.0.1:5000';
const MAX_EVENTS = 5000;

function App() {
  const [token, setToken] = useState(sessionStorage.getItem('token'));
  const [summary, setSummary] = useState(null);
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [connected, setConnected] = useState(false);
  const maxIdRef = useRef(0);
  const [now, setNow] = useState(Date.now());


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
      maxIdRef.current = e.data.events.reduce((m, ev) => Math.max(m, ev.id), 0);
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
    const socket = io(API_URL, { auth: { token }, transports: ['websocket'] });
    socket.on('connect', () => {
      setConnected(true);
      fetchData();
    });
    socket.on('disconnect', () => setConnected(false));
    socket.on('connect_error', () => setConnected(false));
    socket.on('update', (msg) => {
      const fresh = msg.events.filter((ev) => ev.id > maxIdRef.current);
      if (fresh.length) {
        maxIdRef.current = fresh[fresh.length - 1].id;
        setEvents((prev) => [...prev, ...fresh].slice(-MAX_EVENTS));
      }
      setSummary(msg.summary);
      setLastUpdated(new Date().toLocaleTimeString());
    });
    return () => socket.disconnect();
  }, [token, fetchData]);

  const handleLogin = (t) => {
    sessionStorage.setItem('token', t);
    setToken(t);
  };

useEffect(() => {
  const id = setInterval(() => setNow(Date.now()), 10000);
  return () => clearInterval(id);
}, []);

  if (!token) return <Login apiUrl={API_URL} onLogin={handleLogin} />;
  if (error) return <div className="error"><h2>{error}</h2></div>;
  if (!summary) return <div className="loading"><h2>Connecting to Honeypot...</h2></div>;

  const latestMs = events.reduce((m, e) => Math.max(m, Date.parse(e.timestamp) || 0), 0);
  const ageSec = latestMs ? Math.max(0, Math.floor((now - latestMs) / 1000)) : null;
  const stale = ageSec === null || ageSec > 300;
  const ageText = ageSec === null ? 'no events' : ageSec < 60 ? `${ageSec}s ago` : `${Math.floor(ageSec / 60)}m ago`;


  return (
    <div className="app">
      <header className="header">
        <h1>Real-Time Cyber Threat Intelligence Dashboard</h1>
        <p>Mount Kenya University — Honeypot Monitoring System</p>
        <span className="last-updated">
          Last updated: {lastUpdated} ·{' '}
          {connected ? 'Live: WebSocket connected' : 'Live feed disconnected, reconnecting'}
        </span>
        <span className="last-updated" style={{ display: 'block', color: stale ? '#EF4444' : undefined }}>
          Latest event: {latestMs ? new Date(latestMs).toLocaleTimeString() : 'none'} ({ageText}){stale ? ' — data may be stale' : ''}
        </span>
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
