# tkz

Shared tokenizer used by the indexer and API.

```python
import tkz
tkz.tokenize("Search the web, fast.")
# -> ["search", "web", "fast"]
```

`tokenize(text)` lowercases input, extracts alphanumeric words, and drops English NLTK stop words. Returns `[]` for empty input.

NLTK stop words are cached in `/tmp/nltk_data` and downloaded on first use.

## Used by

- `apps/index` — building `quickly_word_index` rows.
- `apps/api` — tokenizing incoming queries.
