import db
import schema


def init_db():
    conn = db.get_db()
    conn.execute(schema.init)
    conn.commit()


def drop_db():
    conn = db.get_db()
    conn.execute(schema.drop)
    conn.commit()
