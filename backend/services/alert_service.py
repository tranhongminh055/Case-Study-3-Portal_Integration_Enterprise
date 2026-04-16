from backend.database.session import SessionSqlServer, SessionMysql
from backend.repositories import alert_repository as repo
from backend.utils.logger import logger


def get_alerts():
    with SessionSqlServer() as sql_session, SessionMysql() as mysql_session:
        def _split_name(full_name: str):
            if not full_name:
                return "", ""
            parts = full_name.strip().split()
            if len(parts) == 1:
                return parts[0], ""
            return " ".join(parts[:-1]), parts[-1]

        # anniversaries
        anniversaries = []
        try:
            for emp in repo.anniversary_alerts(sql_session):
                first, last = _split_name(getattr(emp, "full_name", None) or "")
                anniversaries.append({
                    "employee_id": emp.id,
                    "name": f"{first} {last}".strip(),
                    "hire_date": emp.hire_date.isoformat() if emp.hire_date else None,
                })
        except Exception as e:
            logger.exception("Failed to load anniversary alerts: %s", e)

        # abnormal salaries
        abnormal_salaries = []
        try:
            for salary in repo.abnormal_salary_alerts(mysql_session):
                abnormal_salaries.append({
                    "employee_id": salary.employee_id,
                    "amount": float(salary.amount),
                    "effective_date": salary.effective_date.isoformat() if salary.effective_date else None,
                })
        except Exception as e:
            logger.exception("Failed to load abnormal salary alerts: %s", e)

        # excessive leave
        excessive = []
        try:
            excessive = repo.excessive_leave_alerts(mysql_session)
        except Exception as e:
            logger.exception("Failed to load excessive leave alerts: %s", e)

        return {
            "anniversaries": anniversaries,
            "abnormal_salaries": abnormal_salaries,
            "excessive_leave": excessive,
        }
