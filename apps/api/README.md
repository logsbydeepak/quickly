# API

Flask `/search` endpoint backing the frontend.

## Endpoint

`GET /search?q=<query>&page=1&page_size=10` (`page_size` capped at 50).

```json
{
  "results": [{ "url": "...", "title": "...", "description": "...", "score": 12, "exact_match": false }],
  "meta": { "query": "...", "search_speed_ms": 6.1, "total_results": 1 },
  "pagination": { "page": 1, "page_size": 10, "total_pages": 1, "has_next": false, "has_previous": false }
}
```

## Ranking

Tokenize query with `tkz`, look up `quickly_word_index`, join page metadata, count backlinks, then sort by:

1. Exact URL match (pinned to top, tagged `exact_match: true`)
2. Distinct query words in title
3. Distinct query words in description
4. Distinct query words anywhere
5. Keyword score (title/description weighted at index time)
6. Backlink count
7. Title

Domain-like queries (`google.com`, `https://...`) are matched against URL variants with/without `www.`, `http`/`https`, and trailing slash.

## Run

```sh
export DB_URL="postgresql://user:pass@localhost:5432/quickly"
make api                                # from repo root
# or
uv run flask --app main run             # from this dir
```

Permissive CORS is enabled for local dev.
