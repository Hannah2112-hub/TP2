import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    _connection_params = None

    @classmethod
    def get_connection_params(cls) -> dict:
        if cls._connection_params is None:
            url = getenv("DATABASE_URL", "")
            parts = url.replace("postgresql://", "").split("@")
            user_pass = parts[0].split(":")
            host_db = parts[1].split("/")
            host_port = host_db[0].split(":")

            cls._connection_params = {
                "host": host_port[0],
                "port": int(host_port[1]) if len(host_port) > 1 else 5432,
                "database": host_db[1],
                "user": user_pass[0],
                "password": user_pass[1],
            }
        return cls._connection_params


@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DatabaseConfig.get_connection_params())
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query: str, params: list = None):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or [])
            conn.commit()
            query_upper = query.strip().upper()
            if query_upper.startswith("SELECT"):
                return [dict(row) for row in cursor.fetchall()]
            if cursor.description:
                return [dict(row) for row in cursor.fetchall()]
            return []
