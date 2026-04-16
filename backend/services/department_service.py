from backend.database.session import SessionSqlServer
from backend.repositories import department_repository as repo
from backend.services.transaction_manager import cross_db_transaction
from backend.utils.errors import NotFoundError
from backend.utils.logger import logger


def list_departments():
    with SessionSqlServer() as session:
        return repo.list_departments(session)


def get_department(department_id):
    with SessionSqlServer() as session:
        department = repo.get_department(session, department_id)
        if not department:
            raise NotFoundError(f"Department {department_id} not found")
        return department


def create_department(payload):
    with cross_db_transaction() as (sql_session, mysql_session, compensations):
        department = repo.create_department(sql_session, payload)

        def _comp_delete_sql():
            from backend.database.session import SessionSqlServer
            with SessionSqlServer() as s:
                dep = repo.get_department(s, department.id)
                if dep:
                    repo.delete_department(s, dep)
                    s.commit()

        compensations.append(_comp_delete_sql)

        mysql_payload = {**payload, "id": department.id}
        repo.create_department_mysql(mysql_session, mysql_payload)
        logger.info("Created department %s in SQL Server and MySQL", department.id)
        return department


def update_department(department_id, payload):
    with cross_db_transaction() as (sql_session, mysql_session, compensations):
        department = repo.get_department(sql_session, department_id)
        if not department:
            raise NotFoundError(f"Department {department_id} not found")

        prev = {k: getattr(department, k) for k in payload.keys() if hasattr(department, k)}
        updated = repo.update_department(sql_session, department, payload)

        def _comp_restore_sql():
            from backend.database.session import SessionSqlServer
            with SessionSqlServer() as s:
                dep = repo.get_department(s, department_id)
                if dep:
                    repo.update_department(s, dep, prev)
                    s.commit()

        compensations.append(_comp_restore_sql)

        repo.update_department_mysql(mysql_session, department_id, payload)
        logger.info("Updated department %s in SQL Server and MySQL", department_id)
        return updated


def delete_department(department_id):
    with cross_db_transaction() as (sql_session, mysql_session, compensations):
        department = repo.get_department(sql_session, department_id)
        if not department:
            raise NotFoundError(f"Department {department_id} not found")

        from backend.utils.orm import serialize_model
        prev_data = serialize_model(department)

        def _comp_recreate_sql():
            from backend.database.session import SessionSqlServer
            with SessionSqlServer() as s:
                existing = repo.get_department(s, department_id)
                if not existing:
                    repo.create_department(s, prev_data)
                    s.commit()

        compensations.append(_comp_recreate_sql)

        repo.delete_department(sql_session, department)
        repo.delete_department_mysql(mysql_session, department_id)
        logger.info("Deleted department %s from both databases", department_id)
