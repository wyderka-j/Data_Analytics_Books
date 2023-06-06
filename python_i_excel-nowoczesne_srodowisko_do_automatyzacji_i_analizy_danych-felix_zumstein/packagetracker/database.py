"""Ten moduł obsługuje wszystkie interakcje z bazą danych"""

from pathlib import Path
from sqlite3 import Connection as SQLite3Connection

import sqlalchemy
from sqlalchemy import event
from sqlalchemy.sql import text
from sqlalchemy.engine import Engine
import pandas as pd


# Aby SQLAlchemy wymuszał klucze obce z SQLite, zapoznaj się z instrukcją:
# https://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#foreign-key-support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Chcemy, aby plik bazy danych znajdował się obok tego pliku.
# Tutaj zamieniamy ścieżkę na ścieżkę bezwzględną.
this_dir = Path(__file__).resolve().parent
db_path = this_dir / "packagetracker.db"

# Silnik bazy danych
engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")


def get_packages():
    """Pobieranie wszystkich pakietów jako DataFrame"""

    return pd.read_sql_table("packages", con=engine, index_col="package_id")


def store_package(package_name):
    """Wstaw nazwę nowego pakietu do tabeli packages"""

    try:
        with engine.connect() as con:
            con.execute(text("INSERT INTO packages (package_name) VALUES (:package_name)"),
                        package_name=package_name)
        return None
    except sqlalchemy.exc.IntegrityError:
        return f"{package_name} already exists"
    except Exception as e:
        return repr(e)


def get_versions(package_name):
    """Pobieranie wszystkich wersji pakietu o nazwie package_name"""

    sql = """
    SELECT v.uploaded_at, v.version_string
    FROM packages p
    INNER JOIN package_versions v ON p.package_id = v.package_id
    WHERE p.package_name = :package_name
    """
    return pd.read_sql_query(text(sql), engine, parse_dates=["uploaded_at"],
                             params={"package_name": package_name},
                             index_col=["uploaded_at"])


def store_versions(df):
    """Wstawianie rekordów z dostarczonego DataFrame df do tabeli package_versions"""

    df.to_sql("package_versions", con=engine, if_exists="append", index=False)


def delete_versions():
    """Usunięcie wszystkich rekordów z tabeli zawierającej wersje"""

    with engine.connect() as con:
        con.execute("DELETE FROM package_versions")


def create_db():
    """Uruchom tę funkcję, aby utworzyć tabele bazy danych.
    W przypadku sqlite spowoduje to również utworzenie pliku bazy danych.
    """

    sql_table_packages = """
    CREATE TABLE packages (
        package_id INTEGER PRIMARY KEY,
        package_name TEXT NOT NULL,
        UNIQUE(package_name)
    )
    """

    sql_table_versions = """
    CREATE TABLE package_versions (
        package_id INTEGER,
        version_string TEXT,
        uploaded_at TIMESTAMP NOT NULL,
        PRIMARY KEY (package_id, version_string),
        FOREIGN KEY (package_id) REFERENCES packages (package_id)
    )
    """

    sql_statements = [sql_table_packages, sql_table_versions]
    with engine.connect() as con:
        for sql in sql_statements:
            con.execute(sql)


if __name__ == "__main__":
    # Uruchom to jako skrypt, aby utworzyć bazę danych packagetracker.db
    create_db()
