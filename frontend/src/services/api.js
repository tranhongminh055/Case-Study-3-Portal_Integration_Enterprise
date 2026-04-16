import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const api = axios.create({ baseURL, timeout: 10000 });

export const getEmployees = () => api.get('/employees');
export const getEmployeesWithPayroll = () => api.get('/employees/with-payroll');
export const createEmployee = (payload) => api.post('/employees', payload);
export const updateEmployee = (id, payload) => api.put(`/employees/${id}`, payload);
export const deleteEmployee = (id) => api.delete(`/employees/${id}`);
export const getReports = () => api.get('/reports');
export const getAlerts = () => api.get('/alerts');
export const getSalaries = () => api.get('/salaries');
export const getAttendance = () => api.get('/attendance');
