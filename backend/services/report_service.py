from backend.database.session import SessionSqlServer, SessionMysql
from backend.repositories import report_repository as repo


def get_reports():
    with SessionSqlServer() as sql_session, SessionMysql() as mysql_session:
        return repo.employee_report_data(sql_session, mysql_session)
