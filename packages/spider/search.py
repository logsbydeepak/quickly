import config
import tkz


def search(conn, query):
    words = tkz.tokenize(query)

    rows = conn.execute(
        """
        SELECT
            p.url,
            p.title,
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

    return rows


def main():
    conn = config.init_db()

    results = search(conn, "python")
    for row in results:
        print(row)


if __name__ == "__main__":
    main()
