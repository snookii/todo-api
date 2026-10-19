from pathlib import Path
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "todo.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

def initialize_database():
    sql_path = PROJECT_ROOT / "app" / "schema.sql"
    sql = sql_path.read_text(encoding="utf-8")
    connection = engine.raw_connection()
    try:
        connection.executescript(sql)
        connection.commit()
    finally:
        connection.close()