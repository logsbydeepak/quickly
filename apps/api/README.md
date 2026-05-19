# Quickly API

This Flask app exposes the search endpoint used by the Astro frontend.

## Endpoint

### `GET /search`

Query parameters:

- `q`: search text. Empty values return an empty result set.
- `page`: 1-based page number. Defaults to `1`.
- `page_size`: results per page. Defaults to `10` and is capped at `50`.

Example:

```sh
curl "http://127.0.0.1:5000/search?q=python&page=1"
```

Response shape:

```json
{
  "results": [
    {
      "url": "https://example.com",
      "title": "Example",
      "description": "Short summary",
      "score": 12,
      "exact_match": false
    }
  ],
  "meta": {
    "query": "python",
    "search_speed_ms": 6.1,
    "total_results": 1
  },
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_pages": 1,
    "has_next": false,
    "has_previous": false
  }
}
```

## Ranking

The API tokenizes the query with `tkz`, finds matching rows in `quickly_word_index`, joins page metadata from `quickly_page`, counts backlinks from `quickly_page_link`, and sorts by:

1. Exact URL match (see below)
2. Number of distinct query words found in the page **title**
3. Number of distinct query words found in the page **description**
4. Number of distinct query words matched anywhere (title, description, or body)
5. Keyword score (sum of term frequencies, with title/description already weighted higher at index time)
6. Backlink count
7. Title

## Exact URL match

When the query looks like a domain or URL (e.g. `google.com`, `www.google.com`,
`https://google.com/path`), the API also checks `quickly_page.url` against a set
of normalised candidates: with and without `www.`, `http` and `https`, and with
or without a trailing slash. Any page whose URL matches a candidate is pinned to
the top of the results and tagged with `"exact_match": true`. The exact match is
returned even if the page does not appear in the word index.

## Development

Set `DB_URL` first:

```sh
export DB_URL="postgresql://user:password@localhost:5432/quickly"
```

Run from the repository root:

```sh
make api
```

Or run directly inside this directory:

```sh
uv run flask --app main run
```

The app adds permissive CORS headers so the local Astro frontend can call it during development.
