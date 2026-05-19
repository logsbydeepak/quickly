# Spider

BFS web crawler. Honors `robots.txt`, stores pages and outgoing links in Postgres.

## Run

```sh
export DB_URL="postgresql://user:pass@localhost:5432/quickly"
uv run python main.py <url> [url ...]
```

Each seed runs a BFS capped at 50 fetched pages, with a 1s delay between requests.

## Behavior

- `robots.txt` is fetched once per host and cached in `quickly_robot`.
- Disallowed URLs are skipped.
- Pages are stored in `quickly_page` (url, title, description, body text).
- Outgoing links go into `quickly_page_link`.
- Already-stored URLs are reused from cache, not re-fetched.

## Files

- `main.py` — crawl loop and CLI.
- `utils.py` — fetch, parse, link extraction.
- `db_utils.py` — page / robot / link persistence.
