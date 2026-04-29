from flask import Flask, request, jsonify, g
from psycopg.rows import dict_row
from db import close_db, get_db
import tkz

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    close_db(g)


@app.get("/search")
def hello_world():
    result = []
    query = request.args.get("q", "")
    if not query:
        return jsonify(result)

    words = tkz.tokenize(query)

    db = get_db(g, row_factory=dict_row)

    rows = db.execute(
        """
        SELECT
            p.url,
            p.title,
            p.description,
            SUM(w.frequency) AS keyword_score,
            COUNT(pl.from_url) AS backlinks,
            SUM(w.frequency) + COUNT(pl.from_url) AS total_score
        FROM word_index w
        JOIN page p ON p.id = w.page_id
        LEFT JOIN page_link pl ON pl.to_url = p.url
        WHERE w.word = ANY(%s)
        GROUP BY p.id, p.url, p.title
        ORDER BY total_score DESC
        LIMIT 10;
        """,
        (words,),
    ).fetchall()

    for row in rows:
        result.append(
            {"url": row["url"], "title": row["title"], "description": row["title"]}
        )

    return result
