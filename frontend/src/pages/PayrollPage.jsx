import { useEffect, useState } from 'react';
import { getSalaries, getAttendance } from '../services/api';

export default function PayrollPage() {
  const [salaries, setSalaries] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const [sRes, aRes] = await Promise.all([getSalaries(), getAttendance()]);
        if (!mounted) return;
        setSalaries(sRes.data || []);
        setAttendance(aRes.data || []);
      } catch (err) {
        console.error('Failed to load payroll data', err);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => { mounted = false; };
  }, []);

  if (loading) return <div>Loading payroll data…</div>;

  return (
    <div className="payroll-page">
      <h2>Payroll - Salaries</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Amount</th>
            <th>Currency</th>
            <th>Effective Date</th>
          </tr>
        </thead>
        <tbody>
          {salaries.map((s) => (
            <tr key={s.id || `${s.employee_id}-${s.effective_date}`}>
              <td>{s.employee_id ?? s.EmployeeID ?? ''}</td>
              <td>{s.amount ?? s.Amount ?? ''}</td>
              <td>{s.currency ?? s.Currency ?? ''}</td>
              <td>{s.effective_date ?? s.EffectiveDate ?? ''}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Payroll - Attendance</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Date</th>
            <th>Status</th>
            <th>Hours</th>
          </tr>
        </thead>
        <tbody>
          {attendance.map((a) => (
            <tr key={a.id || `${a.employee_id}-${a.work_date}`}>
              <td>{a.employee_id ?? a.EmployeeID ?? ''}</td>
              <td>{a.work_date ?? a.WorkDate ?? ''}</td>
              <td>{a.status ?? a.Status ?? ''}</td>
              <td>{a.hours ?? a.Hours ?? ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
