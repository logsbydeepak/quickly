# Web

Astro frontend for Quickly. Server-renders results, handles theming, and posts search queries to the API.

## Pages

- `/` — search home with random suggestion chips.
- `/search?q=&page=` — paginated results, related searches, quick facts.

See [`src/pages/README.md`](src/pages/README.md).

## Config

```sh
export PUBLIC_API_URL="http://127.0.0.1:5000"
```

If unset, pages fall back to `http://127.0.0.1:5000`.

## Develop

```sh
bun install
bun run dev          # dev server
bun run build        # production build
bun run preview      # preview build
```
