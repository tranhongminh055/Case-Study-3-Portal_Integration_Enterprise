import { useEffect, useState } from 'react';

function EmployeeForm({ employee, onSubmit }) {
  const [formState, setFormState] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    hire_date: '',
    department_id: '',
    position_id: '',
    status: 'active',
  });

  useEffect(() => {
    if (employee) {
      setFormState({
        first_name: employee.first_name || '',
        last_name: employee.last_name || '',
        email: employee.email || '',
        phone: employee.phone || '',
        hire_date: employee.hire_date || '',
        department_id: employee.department_id ?? '',
        position_id: employee.position_id ?? '',
        status: employee.status || 'active',
      });
    }
  }, [employee]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormState((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const payload = {
      first_name: formState.first_name,
      last_name: formState.last_name,
      email: formState.email,
      phone: formState.phone || null,
      hire_date: formState.hire_date,
      department_id: formState.department_id ? Number(formState.department_id) : null,
      position_id: formState.position_id ? Number(formState.position_id) : null,
      status: formState.status,
    };

    if (employee && employee.id) {
      await onSubmit(employee.id, payload);
    } else {
      await onSubmit(payload);
    }
  };

  const handleReset = () => {
    setFormState({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      hire_date: '',
      department_id: '',
      position_id: '',
      status: 'active',
    });
  };

  return (
    <form className="entity-form" onSubmit={handleSubmit}>
      <label>
        First Name
        <input name="first_name" value={formState.first_name} onChange={handleChange} required />
      </label>
      <label>
        Last Name
        <input name="last_name" value={formState.last_name} onChange={handleChange} required />
      </label>
      <label>
        Email
        <input name="email" type="email" value={formState.email} onChange={handleChange} required />
      </label>
      <label>
        Phone
        <input name="phone" value={formState.phone} onChange={handleChange} />
      </label>
      <label>
        Hire Date
        <input name="hire_date" type="date" value={formState.hire_date} onChange={handleChange} required />
      </label>
      <label>
        Department ID
        <input name="department_id" type="number" value={formState.department_id} onChange={handleChange} />
      </label>
      <label>
        Position ID
        <input name="position_id" type="number" value={formState.position_id} onChange={handleChange} />
      </label>
      <label>
        Status
        <select name="status" value={formState.status} onChange={handleChange}>
          <option value="active">active</option>
          <option value="inactive">inactive</option>
          <option value="terminated">terminated</option>
        </select>
      </label>
      <div className="form-actions">
        <button type="submit">{employee ? 'Update Employee' : 'Create Employee'}</button>
        <button type="button" className="secondary" onClick={handleReset}>
          Clear
        </button>
      </div>
    </form>
  );
}

export default EmployeeForm;
