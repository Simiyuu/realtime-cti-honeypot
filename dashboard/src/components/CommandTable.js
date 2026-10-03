import React from 'react';

function CommandTable({ events }) {
  const commands = events.filter(e => e.event_type === 'cowrie.command.input');
  const logins = events.filter(e => e.event_type === 'cowrie.login.success');
  const downloads = events.filter(e => e.event_type === 'cowrie.session.file_download');

  return (
    <div className="command-table">
      <h2>Attack Intelligence</h2>

      <div className="intel-section">
        <h3>Commands Executed ({commands.length})</h3>
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
              <tr><td colSpan="3">No commands captured yet</td></tr>
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
        <h3>Captured Credentials ({logins.length})</h3>
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
              <tr><td colSpan="4">No credentials captured yet</td></tr>
            ) : (
              logins.map((event, index) => (
                <tr key={index}>
                  <td>{new Date(event.timestamp).toLocaleTimeString()}</td>
                  <td>{event.src_ip}</td>
                  <td>{event.username}</td>
                  <td><code>{event.password}</code></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="intel-section">
        <h3>File Downloads ({downloads.length})</h3>
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
              <tr><td colSpan="3">No downloads captured yet</td></tr>
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
