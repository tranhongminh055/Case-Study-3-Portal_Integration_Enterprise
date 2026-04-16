from backend.models.employee import Employee
from backend.models.salary import Salary
from backend.models.attendance import Attendance


def employee_report_data(sql_session, mysql_session):
    employees = sql_session.query(Employee).order_by(Employee.id).all()
    salary_map = {
        salary.employee_id: float(salary.amount)
        for salary in mysql_session.query(Salary).order_by(Salary.effective_date.desc()).all()
    }
    attendance_map = {}
    for record in mysql_session.query(Attendance).order_by(Attendance.work_date.desc()).all():
        attendance_map.setdefault(record.employee_id, []).append({
            "date": record.work_date.isoformat(),
            "status": record.status,
            "leave_hours": record.leave_hours,
        })

    combined = []
    for employee in employees:
        combined.append({
            "employee_id": employee.id,
            "name": f"{employee.first_name} {employee.last_name}",
            "email": employee.email,
            "department_id": employee.department_id,
            "position_id": employee.position_id,
            "hire_date": employee.hire_date.isoformat() if employee.hire_date else None,
            "salary": salary_map.get(employee.id),
            "attendance": attendance_map.get(employee.id, []),
        })
    return combined
