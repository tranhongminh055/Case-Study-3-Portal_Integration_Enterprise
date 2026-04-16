from backend.database.session import SessionMysql
from backend.repositories import payroll_repository as repo


def list_salaries():
    with SessionMysql() as session:
        return repo.get_all_salaries(session)


def list_attendance():
    with SessionMysql() as session:
        return repo.get_all_attendance(session)
