# db

Shared PostgreSQL helpers and schema.

## Connection

```sh
export DB_URL="postgresql://user:pass@localhost:5432/quickly"
```

- `db.connect(url=None)` — opens a connection (reads `DB_URL` if no URL is passed).
- `db.get_db()` — cached connection for scripts.
- `db.get_db(scope)` — attaches the connection to a scope (used with `flask.g`).

## Tables

- `quickly_page` — crawled page metadata and content.
- `quickly_robot` — cached `robots.txt`.
- `quickly_page_link` — page-to-page links.
- `quickly_word_index` — token frequencies per page.

## Commands

```sh
make init_db                            # create tables
make drop_db                            # drop tables
uv run python sync.py <source> <target> # copy quickly_* rows
```

`sync.py` creates missing tables on the target, clears them, then copies rows from the source URL.
