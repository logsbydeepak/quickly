import os
import psycopg
import schema

db = None
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL environment variable is not set")


def get_db():
    global db
    if db is None:
        db = psycopg.connect(DB_URL)
    return db


def init_db():
    db = get_db()
    db.execute(schema.init)
    db.commit()


def drop_db():
    db = get_db()
    db.execute(schema.drop)
    db.commit()
