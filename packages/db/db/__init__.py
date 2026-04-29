import os

import psycopg

_db = None


def connect(db_url=None, **kwargs):
    url = db_url or os.getenv("DB_URL")
    if not url:
        raise ValueError("DB_URL environment variable is not set")
    return psycopg.connect(url, **kwargs)


def get_db(scope=None, db_url=None, **kwargs):
    if scope is not None:
        if not hasattr(scope, "db"):
            scope.db = connect(db_url, **kwargs)
        return scope.db

    global _db
    if _db is None:
        _db = connect(db_url, **kwargs)
    return _db


def close_db(scope=None):
    if scope is not None:
        db = getattr(scope, "db", None)
        if db is not None:
            db.close()
            delattr(scope, "db")
        return

    global _db
    if _db is not None:
        _db.close()
        _db = None
