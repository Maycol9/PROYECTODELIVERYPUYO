import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_database_uri():
    force_sqlite = os.getenv("FORCE_SQLITE", "true").lower() == "true"

    if force_sqlite:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return f"sqlite:///{os.path.join(base_dir, 'delivery_puyo.db')}"

    host = os.getenv("DB_HOST") or os.getenv("MYSQLHOST")
    port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or "3306"
    user = os.getenv("DB_USER") or os.getenv("MYSQLUSER")
    password = quote_plus(os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD") or "")
    database = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE")

    if host and user and database:
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    return f"sqlite:///{os.path.join(base_dir, 'delivery_puyo.db')}"
