import argparse

import psycopg
from psycopg import sql

import schema


TABLES = [
    "quickly_page",
    "quickly_robot",
    "quickly_page_link",
    "quickly_word_index",
]


def get_columns(conn, table):
    rows = conn.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    ).fetchall()
    return [row[0] for row in rows]


def clear_tables(conn):
    for table in reversed(TABLES):
        conn.execute(sql.SQL("TRUNCATE TABLE {} CASCADE").format(sql.Identifier(table)))


def copy_table(source, target, table):
    columns = get_columns(source, table)
    if not columns:
        print(f"skip {table}: table not found in source")
        return

    rows = source.execute(
        sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.Identifier(table),
        )
    ).fetchall()

    if not rows:
        print(f"{table}: 0 rows")
        return

    insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(", ").join(map(sql.Identifier, columns)),
        sql.SQL(", ").join(sql.Placeholder() for _ in columns),
    )
    with target.cursor() as cursor:
        cursor.executemany(insert_sql, rows)
    print(f"{table}: {len(rows)} rows")


def sync(source_url, target_url):
    with psycopg.connect(source_url) as source:
        with psycopg.connect(target_url) as target:
            target.execute(schema.init)
            clear_tables(target)

            for table in TABLES:
                copy_table(source, target, table)

            target.commit()


def main():
    parser = argparse.ArgumentParser(
        description="Sync Quickly table data from one Postgres database to another."
    )
    parser.add_argument(
        "source_url", help="Source Postgres URL, for example local psql"
    )
    parser.add_argument("target_url", help="Target Postgres URL, for example Supabase")
    args = parser.parse_args()

    sync(args.source_url, args.target_url)


if __name__ == "__main__":
    main()
