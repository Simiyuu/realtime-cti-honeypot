import React from 'react';

function SummaryCards({ summary }) {
  if (!summary) return null;

  const cards = [
    {
      title: 'Total Connections',
      value: summary.total_connections,
      label: 'CONNECTIONS',
      color: '#3B82F6'
    },
    {
      title: 'Successful Logins',
      value: summary.successful_logins,
      label: 'LOGINS',
      color: '#EF4444'
    },
    {
      title: 'Commands Executed',
      value: summary.commands_executed,
      label: 'COMMANDS',
      color: '#F59E0B'
    },
    {
      title: 'File Downloads',
      value: summary.file_downloads,
      label: 'DOWNLOADS',
      color: '#10B981'
    },
    { 
      title: 'Failed Logins', value: summary.failed_logins, label: 'FAILED', color: '#EC4899' 
    },
    { 
      title: 'Sessions Closed', value: summary.sessions_closed, label: 'CLOSED', color: '#64748B'
    },
    {
      title: 'Total Events',
      value: summary.total_events,
      label: 'EVENTS',
      color: '#8B5CF6'
    }
  ];

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div
          key={index}
          className="card"
          style={{ borderTop: `3px solid ${card.color}` }}
        >
          <div
            className="card-label"
            style={{ color: card.color }}
          >
            {card.label}
          </div>
          <div className="card-value">{card.value}</div>
          <div className="card-title">{card.title}</div>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;