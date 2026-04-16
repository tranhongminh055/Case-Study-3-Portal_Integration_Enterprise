import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import SQLAlchemyError

from backend.utils.logger import logger

# Load backend .env before reading database settings.
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

SQLSERVER_DRIVER = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")
SQLSERVER_SERVER = os.getenv("SQLSERVER_SERVER", "localhost")
SQLSERVER_DATABASE = os.getenv("SQLSERVER_DATABASE", "HUMAN")
SQLSERVER_UID = os.getenv("SQLSERVER_UID")
SQLSERVER_PWD = os.getenv("SQLSERVER_PWD")
# When true, use Windows Integrated Security / Trusted Connection (no UID/PWD)
USE_TRUSTED_CONNECTION = os.getenv("USE_TRUSTED_CONNECTION", "false").lower() == "true"
# Control ODBC encryption behaviour (ODBC Driver 18 defaults to Encrypt=YES)
SQLSERVER_ENCRYPT = os.getenv("SQLSERVER_ENCRYPT", "no").lower()  # 'yes' or 'no'
# When true, allow falling back to a local SQLite file if SQL Server cannot be reached.
# This must be explicitly enabled in environments where fallback is acceptable.
FALLBACK_TO_SQLITE = os.getenv("FALLBACK_TO_SQLITE", "false").lower() == "true"

# Build the ODBC connection string using the configured server value (allow instance names)
def _normalize_server_name(server: str) -> str:
    # Allow using ".\\INSTANCE" in .env by converting leading dot to localhost
    if server.startswith(".\\"):
        return server.replace(".", "localhost", 1)
    return server


def _build_odbc(driver: str, server: str, database: str, uid: str, pwd: str, trusted: bool, encrypt: str) -> str:
    if trusted:
        return (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes;Encrypt={encrypt};TrustServerCertificate=YES;"
        )
    else:
        return (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={uid};"
            f"PWD={pwd};"
            f"Encrypt={encrypt};TrustServerCertificate=YES;"
        )


# Normalize the server value so instance names like ".\\SQLEXPRESS" become usable
SQLSERVER_SERVER = _normalize_server_name(SQLSERVER_SERVER)

# Try a list of drivers: prefer configured driver but fall back to common ones
driver_candidates = [SQLSERVER_DRIVER, "ODBC Driver 17 for SQL Server", "ODBC Driver 13 for SQL Server", "SQL Server"]
driver_candidates = [d for d in driver_candidates if d]

# Fall back UID/PWD defaults
uid = SQLSERVER_UID or "sa"
pwd = SQLSERVER_PWD or "YourStrong!Passw0rd"

engine = None
last_error = None
for drv in driver_candidates:
    try:
        odbc_str = _build_odbc(drv, SQLSERVER_SERVER, SQLSERVER_DATABASE, uid, pwd, USE_TRUSTED_CONNECTION, SQLSERVER_ENCRYPT)
        connection_url = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str)
        engine = create_engine(connection_url, poolclass=NullPool, future=True)
        # Test connection now so failures are visible early
        with engine.connect() as conn:
            pass
        logger.info("Connected to SQL Server using driver '%s' at %s", drv, SQLSERVER_SERVER)
        break
    except SQLAlchemyError as e:
        last_error = e
        logger.warning("Driver '%s' failed to connect to %s: %s", drv, SQLSERVER_SERVER, e)

if engine is None:
    msg = f"Could not connect to SQL Server at {SQLSERVER_SERVER} using drivers {driver_candidates}."
    logger.error(msg + " Last error: %s", last_error)
    if FALLBACK_TO_SQLITE:
        logger.warning("FALLBACK_TO_SQLITE enabled — creating local SQLite fallback database.")
        sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'dev_sqlserver_fallback.db')
        sqlite_url = f"sqlite:///{sqlite_path}"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, future=True)
    else:
        # Re-raise a clear exception so the application startup fails loudly (500s will show a clear cause)
        raise SQLAlchemyError(msg) from last_error
