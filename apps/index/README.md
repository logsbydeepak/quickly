# Indexer

Tokenizes crawled pages and writes weighted terms to `quickly_word_index`.

## Weights

- Title: 5 per word
- Description: 3 per word
- Body: 1 per word

## Run

```sh
export DB_URL="postgresql://user:pass@localhost:5432/quickly"
make index_all
```

Or directly:

```sh
uv run python -c "import main; main.index_all_pages()"
```

Pages already present in `quickly_word_index` are skipped. To re-index a page, delete its rows first.
