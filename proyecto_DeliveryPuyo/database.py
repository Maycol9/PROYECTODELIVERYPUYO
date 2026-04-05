import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _normalize_uri(uri: str) -> str:
    if uri.startswith("mysql://"):
        return uri.replace("mysql://", "mysql+mysqlconnector://", 1)
    return uri


def get_database_uri() -> str:
    direct_uri = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
        or os.getenv("MYSQL_URL")
    )

    if direct_uri:
        return _normalize_uri(direct_uri)

    host = os.getenv("DB_HOST") or os.getenv("MYSQLHOST")
    port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT")
    user = os.getenv("DB_USER") or os.getenv("MYSQLUSER")
    password = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD")
    database = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE")

    if host and user and database:
        password = quote_plus(password or "")
        port = port or "3306"
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    return f"sqlite:///{os.path.join(base_dir, 'delivery_puyo.db')}"
