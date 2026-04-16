import { useEffect, useState } from 'react';
import { getAlerts } from '../services/api';

function AlertPanel() {
  const [alerts, setAlerts] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await getAlerts();
        setAlerts(response.data);
      } catch (err) {
        setError('Unable to load alerts.');
      }
    };
    fetchAlerts();
  }, []);

  return (
    <section className="alerts-bar">
      <div className="alerts-title">Alerts</div>
      {error && <div className="alert-error">{error}</div>}
      {alerts ? (
        <div className="alerts-summary">
          <span>Anniversaries: {alerts.anniversaries.length}</span>
          <span>Abnormal Salaries: {alerts.abnormal_salaries.length}</span>
          <span>Excessive Leave: {alerts.excessive_leave.length}</span>
        </div>
      ) : (
        <div>Loading alerts...</div>
      )}
    </section>
  );
}

export default AlertPanel;
