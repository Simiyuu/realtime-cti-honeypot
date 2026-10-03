import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SummaryCards from './components/SummaryCards';
import EventFeed from './components/EventFeed';
import CommandTable from './components/CommandTable';
import AttackChart from './components/AttackChart';
import GeoTable from './components/GeoTable';
import './App.css';

const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [summary, setSummary] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchData = async () => {
    try {
      const [summaryRes, eventsRes] = await Promise.all([
        axios.get(`${API_URL}/api/summary`),
        axios.get(`${API_URL}/api/events`)
      ]);
      setSummary(summaryRes.data);
      setEvents(eventsRes.data.events);
      setLastUpdated(new Date().toLocaleTimeString());
      setError(null);
    } catch (err) {
      setError('Cannot connect to honeypot API. Make sure Flask is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return (
    <div className="loading">
      <h2>Connecting to Honeypot...</h2>
    </div>
  );

  if (error) return (
    <div className="error">
      <h2>⚠ {error}</h2>
    </div>
  );

  return (
    <div className="app">
      <header className="header">
        <h1>Real-Time Cyber Threat Intelligence Dashboard</h1>
        <p>Mount Kenya University — Honeypot Monitoring System</p>
        <span className="last-updated">Last updated: {lastUpdated}</span>
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
