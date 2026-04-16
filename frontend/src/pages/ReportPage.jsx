import { useEffect, useState } from 'react';
import { getReports, getAlerts } from '../services/api';

function ReportPage() {
  const [reports, setReports] = useState([]);
  const [alerts, setAlerts] = useState(null);
  const [error, setError] = useState(null);

  const loadReports = async () => {
    try {
      const [reportResponse, alertResponse] = await Promise.all([getReports(), getAlerts()]);
      setReports(reportResponse.data);
      setAlerts(alertResponse.data);
      setError(null);
    } catch (err) {
      setError('Unable to load reports and alerts.');
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  return (
    <section className="page-section">
      <h2>Reports & Alerts</h2>
      {error && <div className="flash-message">{error}</div>}
      <div className="page-grid">
        <div className="card full-card">
          <h3>Combined Employee Report</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Salary</th>
                <th>Attendance Records</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((row) => (
                <tr key={row.employee_id}>
                  <td>{row.employee_id}</td>
                  <td>{row.name}</td>
                  <td>{row.email}</td>
                  <td>{row.salary ?? 'N/A'}</td>
                  <td>{row.attendance.length}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {alerts && (
          <div className="card full-card">
            <h3>Alerts</h3>
            <pre>{JSON.stringify(alerts, null, 2)}</pre>
          </div>
        )}
      </div>
    </section>
  );
}

export default ReportPage;
