from backend.models.salary import Salary
from backend.models.attendance import Attendance


def get_all_salaries(session):
    return session.query(Salary).order_by(Salary.id).all()


def get_all_attendance(session):
    return session.query(Attendance).order_by(Attendance.work_date.desc()).all()


def get_salary_by_employee(session, employee_id):
    return session.query(Salary).filter(Salary.employee_id == employee_id).order_by(Salary.effective_date.desc()).all()


def get_attendance_by_employee(session, employee_id):
    return session.query(Attendance).filter(Attendance.employee_id == employee_id).order_by(Attendance.work_date.desc()).all()


def get_recent_salary(session):
    return session.query(Salary).order_by(Salary.effective_date.desc()).limit(100).all()


def get_recent_attendance(session):
    return session.query(Attendance).order_by(Attendance.work_date.desc()).limit(100).all()
