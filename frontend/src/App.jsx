import { useState } from 'react';
import EmployeePage from './pages/EmployeePage';
import ReportPage from './pages/ReportPage';
import PayrollPage from './pages/PayrollPage';
import AlertPanel from './components/AlertPanel';

function App() {
  const [activeTab, setActiveTab] = useState('employees');

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Enterprise Integration Portal</h1>
        <nav>
          <button onClick={() => setActiveTab('employees')} className={activeTab === 'employees' ? 'active' : ''}>
            Employees
          </button>
          <button onClick={() => setActiveTab('reports')} className={activeTab === 'reports' ? 'active' : ''}>
            Reports
          </button>
          <button onClick={() => setActiveTab('payroll')} className={activeTab === 'payroll' ? 'active' : ''}>
            Payroll
          </button>
        </nav>
      </header>

      <main>
        <AlertPanel />
        {activeTab === 'employees' && <EmployeePage />}
        {activeTab === 'reports' && <ReportPage />}
        {activeTab === 'payroll' && <PayrollPage />}
      </main>
    </div>
  );
}

export default App;
