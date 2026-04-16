from backend.database.session import SessionSqlServer
from backend.repositories import position_repository as repo
from backend.services.transaction_manager import cross_db_transaction
from backend.utils.errors import NotFoundError
from backend.utils.logger import logger


def list_positions():
    with SessionSqlServer() as session:
        return repo.list_positions(session)


def get_position(position_id):
    with SessionSqlServer() as session:
        position = repo.get_position(session, position_id)
        if not position:
            raise NotFoundError(f"Position {position_id} not found")
        return position


def create_position(payload):
    with cross_db_transaction() as (sql_session, mysql_session, compensations):
        position = repo.create_position(sql_session, payload)

        def _comp_delete_sql():
            from backend.database.session import SessionSqlServer
            with SessionSqlServer() as s:
                pos = repo.get_position(s, position.id)
                if pos:
                    repo.delete_position(s, pos)
                    s.commit()

        compensations.append(_comp_delete_sql)

        mysql_payload = {**payload, "id": position.id}
        repo.create_position_mysql(mysql_session, mysql_payload)
        logger.info("Created position %s in SQL Server and MySQL", position.id)
        return position


def update_position(position_id, payload):
    with cross_db_transaction() as (sql_session, mysql_session, compensations):
        position = repo.get_position(sql_session, position_id)
        if not position:
            raise NotFoundError(f"Position {position_id} not found")

        prev = {k: getattr(position, k) for k in payload.keys() if hasattr(position, k)}
        updated = repo.update_position(sql_session, position, payload)

        def _comp_restore_sql():
            from backend.database.session import SessionSqlServer
            with SessionSqlServer() as s:
                pos = repo.get_position(s, position_id)
                if pos:
                    repo.update_position(s, pos, prev)
                    s.commit()

        compensations.append(_comp_restore_sql)

        repo.update_position_mysql(mysql_session, position_id, payload)
        logger.info("Updated position %s in SQL Server and MySQL", position_id)
        return updated


def delete_position(position_id):
    with cross_db_transaction() as (sql_session, mysql_session, compensations):
        position = repo.get_position(sql_session, position_id)
        if not position:
            raise NotFoundError(f"Position {position_id} not found")

        from backend.utils.orm import serialize_model
        prev_data = serialize_model(position)

        def _comp_recreate_sql():
            from backend.database.session import SessionSqlServer
            with SessionSqlServer() as s:
                existing = repo.get_position(s, position_id)
                if not existing:
                    repo.create_position(s, prev_data)
                    s.commit()

        compensations.append(_comp_recreate_sql)

        repo.delete_position(sql_session, position)
        repo.delete_position_mysql(mysql_session, position_id)
        logger.info("Deleted position %s from both databases", position_id)
