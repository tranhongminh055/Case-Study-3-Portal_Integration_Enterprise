import { useEffect, useState } from 'react';
import { getEmployeesWithPayroll, createEmployee, updateEmployee, deleteEmployee } from '../services/api';
import EmployeeForm from '../components/EmployeeForm';
import EmployeeList from '../components/EmployeeList';

function EmployeePage() {
  const [employees, setEmployees] = useState([]);
  const [selected, setSelected] = useState(null);
  const [message, setMessage] = useState(null);

  const loadEmployees = async () => {
    try {
      const response = await getEmployeesWithPayroll();
      setEmployees(response.data);
    } catch (error) {
      setMessage('Unable to load employees.');
    }
  };

  useEffect(() => {
    loadEmployees();
  }, []);

  const handleCreate = async (record) => {
    // client-side uniqueness check to avoid unnecessary API calls
    if (record.email) {
      const exists = employees.some((e) => e.email && e.email.toLowerCase() === record.email.toLowerCase());
      if (exists) {
        setMessage('Email already used by another employee');
        return;
      }
    }
    try {
      await createEmployee(record);
      await loadEmployees();
      setMessage('Employee created successfully.');
    } catch (error) {
      setMessage(error?.response?.data?.message || 'Create failed.');
    }
  };

  const handleUpdate = async (id, record) => {
    // client-side uniqueness check (exclude current record)
    if (record.email) {
      const exists = employees.some((e) => e.email && e.email.toLowerCase() === record.email.toLowerCase() && e.id !== id);
      if (exists) {
        setMessage('Email already used by another employee');
        return;
      }
    }
    try {
      await updateEmployee(id, record);
      await loadEmployees();
      setSelected(null);
      setMessage('Employee updated successfully.');
    } catch (error) {
      setMessage(error?.response?.data?.message || 'Update failed.');
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteEmployee(id);
      await loadEmployees();
      setMessage('Employee deleted successfully.');
    } catch (error) {
      setMessage(error?.response?.data?.message || 'Delete failed. Employee may have existing salary/dividend links.');
    }
  };

  return (
    <section className="page-section">
      <h2>Employee Management</h2>
      {message && <div className="flash-message">{message}</div>}
      <div className="page-grid">
        <div className="card">
          <h3>Create / Update Employee</h3>
          <EmployeeForm employee={selected} onSubmit={selected ? handleUpdate : handleCreate} />
        </div>
        <div className="card">
          <h3>Employees</h3>
          <EmployeeList employees={employees} onEdit={setSelected} onDelete={handleDelete} />
        </div>
      </div>
    </section>
  );
}

export default EmployeePage;
