import React from 'react';

function GeoTable({ events }) {
  const processGeoData = () => {
    const countries = {};

    events.forEach(event => {
      if (!event.geolocation) return;
      
      const geo = event.geolocation;
      
      if (geo.is_private) return;

      const country = geo.country;
      const countryCode = geo.country_code;

      if (!countries[country]) {
        countries[country] = {
          country: country,
          country_code: countryCode,
          city: geo.city,
          isp: geo.isp,
          event_count: 0,
          attack_types: new Set()
        };
      }

      countries[country].event_count += 1;
      countries[country].attack_types.add(event.event_type);
    });

    return Object.values(countries)
      .map(c => ({
        ...c,
        attack_types: Array.from(c.attack_types)
      }))
      .sort((a, b) => b.event_count - a.event_count);
  };

  const getAttackTypeLabel = (type) => {
    switch (type) {
      case 'cowrie.login.success': return 'LOGIN';
      case 'cowrie.login.failed': return 'BRUTE FORCE';
      case 'cowrie.command.input': return 'COMMAND';
      case 'cowrie.session.file_download': return 'DOWNLOAD';
      case 'cowrie.session.connect': return 'SCAN';
      default: return type;
    }
  };

  const getAttackTypeColor = (type) => {
    switch (type) {
      case 'cowrie.login.success': return '#EF4444';
      case 'cowrie.login.failed': return '#F59E0B';
      case 'cowrie.command.input': return '#3B82F6';
      case 'cowrie.session.file_download': return '#10B981';
      case 'cowrie.session.connect': return '#8B5CF6';
      default: return '#64748b';
    }
  };

  const geoData = processGeoData();

  return (
    <div className="geo-table">
      <div className="section-header">
        <h2>Attacker Geolocation</h2>
      </div>

      {geoData.length === 0 ? (
        <div className="geo-empty">
          <p>No external attackers detected yet</p>
          <p className="geo-empty-sub">
            All current activity is from local network — 
            deploy to VPS to capture real external attackers
          </p>
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Country</th>
              <th>City</th>
              <th>ISP</th>
              <th>Events</th>
              <th>Attack Types</th>
            </tr>
          </thead>
          <tbody>
            {geoData.map((entry, index) => (
              <tr key={index}>
                <td>
                  <span className="country-code">{entry.country_code}</span>
                  {entry.country}
                </td>
                <td>{entry.city}</td>
                <td className="isp-cell">{entry.isp}</td>
                <td>
                  <span className="event-count-badge">{entry.event_count}</span>
                </td>
                <td>
                  <div className="attack-types">
                    {entry.attack_types.map((type, i) => (
                      <span
                        key={i}
                        className="attack-type-tag"
                        style={{ borderColor: getAttackTypeColor(type), color: getAttackTypeColor(type) }}
                      >
                        {getAttackTypeLabel(type)}
                      </span>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default GeoTable;
