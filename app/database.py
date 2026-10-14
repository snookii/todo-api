from pathlib import Path
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "todo.db"

engine = create_engine(f"sqlite:///{DB_PATH}")