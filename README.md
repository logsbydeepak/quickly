# Quickly

Quickly is a small search engine workspace. It crawls pages, stores page metadata and links, builds a token index, exposes search results through a Flask API, and renders a fast Astro web UI.

![Quickly search UI screenshot](screenshot.png)

## Workspace

```text
apps/
  api/      Flask JSON API for `/search`
  index/    Batch indexer that turns stored pages into searchable words
  spider/   Crawler that discovers and stores pages
  www/      Astro frontend for the home and results pages
packages/
  db/       Shared PostgreSQL connection helpers and schema
  tkz/      Tokenizer used by the API and indexer
```

## Requirements

- Python 3.12+
- uv
- Bun
- Node.js 22.12+
- PostgreSQL database available through `DB_URL`

## Environment

Set `DB_URL` before running the Python services:

```sh
export DB_URL="postgresql://user:password@localhost:5432/quickly"
```

The web app reads the API location from `PUBLIC_API_URL`. If it is not set, the pages default to a local API:

```sh
export PUBLIC_API_URL="http://127.0.0.1:5000"
```

## Setup

Install Python workspace dependencies:

```sh
uv sync
```

Install frontend dependencies:

```sh
cd apps/www
bun install
```

Initialize the database tables:

```sh
cd packages/db
make init_db
```

## Run The Stack

Start the API from the repository root:

```sh
make api
```

Start the frontend:

```sh
cd apps/www
bun run dev
```

Then open the Astro dev URL and search from the home page.

## Build Search Data

Use the crawler to store pages:

```sh
cd apps/spider
uv run python main.py "https://example.com" --max-pages 25 --max-depth 2
```

Build the word index after pages have been crawled:

```sh
cd apps/index
make index_all
```

Search results are ranked from token frequency and backlink count in `apps/api/main.py`.

## Useful Commands

```sh
make format        # format Python and frontend files
make api           # run the Flask API
cd apps/www && bun run build
cd apps/www && bun run preview
cd packages/db && make drop_db
```

## Documentation

- [Frontend app](apps/www/README.md)
- [Frontend pages](apps/www/src/pages/README.md)
- [Search API](apps/api/README.md)
- [Crawler](apps/spider/README.md)
- [Indexer](apps/index/README.md)
- [Database package](packages/db/README.md)
- [Tokenizer package](packages/tkz/README.md)
