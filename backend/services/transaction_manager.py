from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from backend.database.session import SessionSqlServer, SessionMysql
from backend.utils.logger import logger

@contextmanager
def cross_db_transaction():
    sql_session = SessionSqlServer()
    mysql_session = SessionMysql()
    sql_transaction = None
    mysql_transaction = None
    use_twophase = True
    compensations = []
    try:
        try:
            sql_transaction = sql_session.begin_twophase()
            mysql_transaction = mysql_session.begin_twophase()
        except Exception as exc:
            logger.warning("Two-phase commit not available, falling back to local transaction: %s", exc)
            sql_transaction = sql_session.begin()
            mysql_transaction = mysql_session.begin()
            use_twophase = False

        # provide a place for callers to register compensation callbacks
        yield sql_session, mysql_session, compensations

        if use_twophase:
            sql_transaction.prepare()
            mysql_transaction.prepare()
            sql_transaction.commit()
            mysql_transaction.commit()
        else:
            # best-effort local commit with compensation callbacks
            try:
                sql_session.commit()
            except Exception as e:
                # if committing sql failed, ensure mysql is rolled back
                try:
                    mysql_session.rollback()
                except Exception:
                    logger.exception("Failed to rollback MySQL after SQL commit failure")
                raise

            try:
                mysql_session.commit()
            except Exception as e:
                # MySQL commit failed after SQL commit — attempt compensating actions
                logger.exception("MySQL commit failed after SQL commit — attempting compensations: %s", e)
                try:
                    mysql_session.rollback()
                except Exception:
                    logger.exception("Failed to rollback MySQL after commit failure")

                # Attempt to undo SQL Server changes via registered compensation callbacks
                for comp in reversed(compensations):
                    try:
                        comp(sql_session)
                    except Exception:
                        logger.exception("Compensation callback failed")

                # Try to commit the compensation changes on SQL Server so the system is left consistent
                try:
                    sql_session.commit()
                except Exception:
                    logger.exception("Failed to commit SQL Server compensations")

                # After attempting compensation, raise to signal overall failure so callers/tests see the error
                raise

        logger.info("Cross-database transaction committed successfully.")
    except Exception as err:
        logger.error("Cross-database transaction failed: %s", err)
        try:
            if sql_transaction is not None:
                sql_transaction.rollback()
            else:
                sql_session.rollback()
            logger.info("SQL Server rollback completed.")
        except Exception as rollback_err:
            logger.exception("Failed to rollback SQL Server: %s", rollback_err)
        try:
            if mysql_transaction is not None:
                mysql_transaction.rollback()
            else:
                mysql_session.rollback()
            logger.info("MySQL rollback completed.")
        except Exception as rollback_err:
            logger.exception("Failed to rollback MySQL: %s", rollback_err)
        raise
    finally:
        mysql_session.close()
        sql_session.close()
