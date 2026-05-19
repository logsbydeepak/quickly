# Quickly

A small search engine. Crawl pages, index tokens, serve results.

![screenshot](screenshot.png)

## Architecture

```text
                  ┌─────────────┐
                  │   Web (UI)  │   apps/www  (Astro)
                  └──────┬──────┘
                         │ HTTP  (PUBLIC_API_URL)
                         ▼
                  ┌─────────────┐
                  │  Search API │   apps/api  (Flask)
                  └──────┬──────┘
                         │ SQL
                         ▼
                  ┌─────────────┐
                  │ PostgreSQL  │   packages/db  (schema + conn)
                  └──────▲──────┘
                         │ writes
        ┌────────────────┼────────────────┐
        │                                 │
 ┌──────┴──────┐                   ┌──────┴──────┐
 │   Spider    │  crawls web  ───▶ │   Indexer   │  tokenizes pages
 │ apps/spider │                   │ apps/index  │
 └─────────────┘                   └──────┬──────┘
                                          │ uses
                                          ▼
                                   ┌─────────────┐
                                   │  Tokenizer  │  packages/tkz
                                   └─────────────┘
```

## Layout

```text
apps/
  api/      Flask /search API
  index/    Token indexer
  spider/   Crawler
  www/      Astro frontend
  html/     Static HTML prototype
packages/
  db/       Postgres helpers + schema
  tkz/      Tokenizer
```

## Requirements

Python 3.12+, uv, Bun, Node 22.12+, PostgreSQL.

## Setup

```sh
export DB_URL="postgresql://user:pass@localhost:5432/quickly"
uv sync
cd packages/db && make init_db
cd apps/www && bun install
```

## Run

```sh
make api                       # API on :5000
cd apps/www && bun run dev     # Frontend
```

## Build search data

```sh
cd apps/spider && uv run python main.py https://example.com
cd apps/index && make index_all
```

## Useful commands

```sh
make format                    # format Python + frontend
cd apps/www && bun run build
cd packages/db && make drop_db
```

## Docs

- [API](apps/api/README.md)
- [Indexer](apps/index/README.md)
- [Spider](apps/spider/README.md)
- [Web](apps/www/README.md)
- [HTML prototype](apps/html/README.md)
- [db package](packages/db/README.md)
- [tkz package](packages/tkz/README.md)
