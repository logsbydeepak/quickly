import re
from time import perf_counter
from urllib.parse import urlparse

from flask import Flask, request, jsonify, g
from psycopg.rows import dict_row
from db import close_db, get_db
import tkz

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50

DOMAIN_RE = re.compile(
    r"^(?:https?://)?(?:[a-z0-9-]+\.)+[a-z]{2,}(?::\d+)?(?:/.*)?$",
    re.IGNORECASE,
)


def url_candidates(query):
    q = query.strip()
    if not q or " " in q or not DOMAIN_RE.match(q):
        return []

    parsed = urlparse(q if "://" in q else "https://" + q)
    host = parsed.netloc.lower()
    if not host:
        return []
    path = parsed.path or ""

    hosts = {host}
    if host.startswith("www."):
        hosts.add(host[4:])
    else:
        hosts.add("www." + host)

    if path in ("", "/"):
        paths = {"", "/"}
    else:
        stripped = path.rstrip("/")
        paths = {stripped, stripped + "/"}

    candidates = set()
    for scheme in ("https", "http"):
        for h in hosts:
            for p in paths:
                candidates.add(f"{scheme}://{h}{p}")
    return list(candidates)


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


@app.teardown_appcontext
def teardown_db(exception):
    close_db(g)


@app.get("/search")
def search():
    started_at = perf_counter()
    query = request.args.get("q", "").strip()
    page = max(request.args.get("page", default=1, type=int) or 1, 1)
    page_size = request.args.get("page_size", default=DEFAULT_PAGE_SIZE, type=int)
    page_size = min(max(page_size or DEFAULT_PAGE_SIZE, 1), MAX_PAGE_SIZE)

    if not query:
        return jsonify(
            {
                "results": [],
                "meta": {
                    "query": query,
                    "search_speed_ms": round((perf_counter() - started_at) * 1000, 2),
                    "total_results": 0,
                },
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_pages": 0,
                    "has_next": False,
                    "has_previous": False,
                },
            }
        )

    db = get_db(g, row_factory=dict_row)

    candidates = url_candidates(query)
    exact_urls = set()
    if candidates:
        exact_rows = db.execute(
            "SELECT url FROM quickly_page WHERE url = ANY(%s);",
            (candidates,),
        ).fetchall()
        exact_urls = {r["url"] for r in exact_rows}

    words = tkz.tokenize(query)
    rows = []
    if words:
        rows = db.execute(
            """
            SELECT
                p.url,
                p.title,
                p.description,
                SUM(w.frequency) AS keyword_score,
                COUNT(DISTINCT pl.from_url) AS backlinks,
                COUNT(DISTINCT w.word) AS matched_words
            FROM quickly_word_index w
            JOIN quickly_page p ON p.id = w.page_id
            LEFT JOIN quickly_page_link pl ON pl.to_url = p.url
            WHERE w.word = ANY(%s)
            GROUP BY p.id, p.url, p.title, p.description;
            """,
            (words,),
        ).fetchall()

    by_url = {row["url"]: row for row in rows}

    missing = exact_urls - by_url.keys()
    if missing:
        extras = db.execute(
            """
            SELECT
                p.url,
                p.title,
                p.description,
                0 AS keyword_score,
                COUNT(DISTINCT pl.from_url) AS backlinks,
                0 AS matched_words
            FROM quickly_page p
            LEFT JOIN quickly_page_link pl ON pl.to_url = p.url
            WHERE p.url = ANY(%s)
            GROUP BY p.id, p.url, p.title, p.description;
            """,
            (list(missing),),
        ).fetchall()
        for row in extras:
            by_url[row["url"]] = row

    unique_words = set(words)
    for row in by_url.values():
        title_tokens = set(tkz.tokenize(row.get("title") or ""))
        desc_tokens = set(tkz.tokenize(row.get("description") or ""))
        row["title_hits"] = len(unique_words & title_tokens)
        row["description_hits"] = len(unique_words & desc_tokens)

    sorted_rows = sorted(
        by_url.values(),
        key=lambda row: (
            row["url"] in exact_urls,
            row.get("title_hits") or 0,
            row.get("description_hits") or 0,
            row.get("matched_words") or 0,
            row.get("keyword_score") or 0,
            row.get("backlinks") or 0,
            row.get("title") or "",
        ),
        reverse=True,
    )

    total_results = len(sorted_rows)
    total_pages = (total_results + page_size - 1) // page_size
    if total_pages:
        page = min(page, total_pages)
    start = (page - 1) * page_size
    end = start + page_size

    results = []
    for row in sorted_rows[start:end]:
        keyword_score = row.get("keyword_score") or 0
        backlinks = row.get("backlinks") or 0
        results.append(
            {
                "url": row["url"],
                "title": row["title"],
                "description": row["description"],
                "score": int(keyword_score) + int(backlinks),
                "exact_match": row["url"] in exact_urls,
            }
        )

    return jsonify(
        {
            "results": results,
            "meta": {
                "query": query,
                "search_speed_ms": round((perf_counter() - started_at) * 1000, 2),
                "total_results": total_results,
            },
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
        }
    )
