import React from 'react';

function EventFeed({ events }) {
  const getEventStyle = (eventType) => {
    switch (eventType) {
      case 'cowrie.login.success':
        return { color: '#EF4444', label: 'LOGIN SUCCESS' };
      case 'cowrie.login.failed':
        return { color: '#F59E0B', label: 'LOGIN FAILED' };
      case 'cowrie.command.input':
        return { color: '#3B82F6', label: 'COMMAND' };
      case 'cowrie.session.file_download':
        return { color: '#10B981', label: 'FILE DOWNLOAD' };
      case 'cowrie.session.connect':
        return { color: '#8B5CF6', label: 'CONNECTION' };
      case 'cowrie.session.closed':
        return { color: '#475569', label: 'DISCONNECTED' };
      default:
        return { color: '#475569', label: eventType };
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="event-feed">
      <div className="section-header">
        <span className="live-indicator"></span>
        <h2>Live Attack Feed</h2>
      </div>
      <div className="feed-list">
        {events.length === 0 ? (
          <p className="no-events">No events captured yet</p>
        ) : (
          [...events].reverse().map((event, index) => {
            const style = getEventStyle(event.event_type);
            return (
              <div key={index} className="feed-item">
                <div className="feed-item-header">
                  <span
                    className="event-badge"
                    style={{
                      color: style.color,
                      borderLeft: `3px solid ${style.color}`
                    }}
                  >
                    {style.label}
                  </span>
                  <span className="event-time">{formatTime(event.timestamp)}</span>
                </div>
                <div className="event-details">
                  <span className="event-ip">{event.src_ip}</span>
                  {event.geolocation && event.geolocation.country !== 'Local Network' && (
                    <span className="event-location">
                      {event.geolocation.city}, {event.geolocation.country}
                    </span>
                  )}
                  {event.command && (
                    <span className="event-command">{event.command}</span>
                  )}
                  {event.username && (
                    <span className="event-creds">
                      {event.username} / {event.password}
                    </span>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default EventFeed;