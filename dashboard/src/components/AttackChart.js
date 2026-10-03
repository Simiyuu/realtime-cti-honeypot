import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

function AttackChart({ events }) {
  const processChartData = () => {
    const eventCounts = {};

    events.forEach(event => {
      const time = new Date(event.timestamp);
      const timeKey = `${time.getHours()}:${String(time.getMinutes()).padStart(2, '0')}`;

      if (!eventCounts[timeKey]) {
        eventCounts[timeKey] = {
          time: timeKey,
          connections: 0,
          logins: 0,
          commands: 0,
          downloads: 0
        };
      }

      switch (event.event_type) {
        case 'cowrie.session.connect':
          eventCounts[timeKey].connections += 1;
          break;
        case 'cowrie.login.success':
          eventCounts[timeKey].logins += 1;
          break;
        case 'cowrie.command.input':
          eventCounts[timeKey].commands += 1;
          break;
        case 'cowrie.session.file_download':
          eventCounts[timeKey].downloads += 1;
          break;
        default:
          break;
      }
    });

    return Object.values(eventCounts).sort((a, b) =>
      a.time.localeCompare(b.time)
    );
  };

  const data = processChartData();

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="chart-tooltip">
          <p className="tooltip-time">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="attack-chart">
      <div className="section-header">
        <span className="live-indicator"></span>
        <h2>Attack Frequency Timeline</h2>
      </div>
      {data.length === 0 ? (
        <p className="no-events">No data to display yet</p>
      ) : (
        <ResponsiveContainer width="100%" height={250}>
          <BarChart
            data={data}
            margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="time"
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: '#334155' }}
            />
            <YAxis
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: '#334155' }}
              allowDecimals={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '11px', color: '#64748b' }}
            />
            <Bar dataKey="connections" name="Connections" fill="#8B5CF6" radius={[2, 2, 0, 0]} />
            <Bar dataKey="logins" name="Logins" fill="#EF4444" radius={[2, 2, 0, 0]} />
            <Bar dataKey="commands" name="Commands" fill="#3B82F6" radius={[2, 2, 0, 0]} />
            <Bar dataKey="downloads" name="Downloads" fill="#10B981" radius={[2, 2, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default AttackChart;
