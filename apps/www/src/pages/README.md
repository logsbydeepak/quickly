# Pages

Astro routes for the frontend.

- `index.astro` — home page. Renders the logo, search form, and random suggestion chips (via `random-words`).
- `search.astro` — results page (`prerender = false`). Calls `${PUBLIC_API_URL}/search`, renders results, pagination, related searches, and quick facts. Falls back to an empty payload on error.

Both pages read `PUBLIC_API_URL` (defaults to `http://127.0.0.1:5000`).
