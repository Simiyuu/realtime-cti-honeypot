import React from 'react';

function CommandTable({ events }) {
  const commands = events.filter(e => e.event_type === 'cowrie.command.input');
  const logins = events.filter(e => e.event_type === 'cowrie.login.success');
  const downloads = events.filter(e => e.event_type === 'cowrie.session.file_download');

  return (
    <div className="command-table">
      <div className="section-header">
        <h2>Attack Intelligence</h2>
      </div>

      <div className="intel-section">
        <div className="intel-section-header">
          <span className="intel-label commands-label">COMMANDS</span>
          <span className="intel-count">{commands.length} captured</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Source IP</th>
              <th>Command</th>
            </tr>
          </thead>
          <tbody>
            {commands.length === 0 ? (
              <tr><td colSpan="3" className="empty-row">No commands captured yet</td></tr>
            ) : (
              commands.map((event, index) => (
                <tr key={index}>
                  <td>{new Date(event.timestamp).toLocaleTimeString()}</td>
                  <td>{event.src_ip}</td>
                  <td><code>{event.command}</code></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="intel-section">
        <div className="intel-section-header">
          <span className="intel-label credentials-label">CREDENTIALS</span>
          <span className="intel-count">{logins.length} captured</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Source IP</th>
              <th>Username</th>
              <th>Password</th>
            </tr>
          </thead>
          <tbody>
            {logins.length === 0 ? (
              <tr><td colSpan="4" className="empty-row">No credentials captured yet</td></tr>
            ) : (
              logins.map((event, index) => (
                <tr key={index}>
                  <td>{new Date(event.timestamp).toLocaleTimeString()}</td>
                  <td>{event.src_ip}</td>
                  <td><code>{event.username}</code></td>
                  <td><code className="password">{event.password}</code></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="intel-section">
        <div className="intel-section-header">
          <span className="intel-label downloads-label">FILE DOWNLOADS</span>
          <span className="intel-count">{downloads.length} captured</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Source IP</th>
              <th>URL</th>
            </tr>
          </thead>
          <tbody>
            {downloads.length === 0 ? (
              <tr><td colSpan="3" className="empty-row">No downloads captured yet</td></tr>
            ) : (
              downloads.map((event, index) => (
                <tr key={index}>
                  <td>{new Date(event.timestamp).toLocaleTimeString()}</td>
                  <td>{event.src_ip}</td>
                  <td><code>{event.download_url}</code></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default CommandTable;
