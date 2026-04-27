import re
import config
from collections import Counter

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))


def tokenize(text):
    if not text:
        return []

    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def index_page(conn, page_id, title="", description="", content=""):
    counts = Counter()

    for word in tokenize(title):
        counts[word] += 5

    for word in tokenize(description):
        counts[word] += 3

    for word in tokenize(content):
        counts[word] += 1

    rows = [(word, page_id, freq) for word, freq in counts.items()]

    if not rows:
        return

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO word_index(word, page_id, frequency)
            VALUES (%s, %s, %s)
            ON CONFLICT (word, page_id)
            DO UPDATE SET frequency = EXCLUDED.frequency
            """,
            rows,
        )

    conn.commit()


def index_all_pages(conn, batch_size=10):
    total = 0

    while True:
        rows = conn.execute(
            """
            SELECT p.id, p.title, p.description, p.content
            FROM page p
            WHERE NOT EXISTS (
                SELECT 1
                FROM word_index w
                WHERE w.page_id = p.id
            )
            LIMIT %s;
            """,
            (batch_size,),
        ).fetchall()

        if not rows:
            break

        for page_id, title, description, content in rows:
            index_page(conn, page_id, title, description, content)

        conn.commit()

        total += len(rows)
        print(f"Indexed {total} pages")

    print("All pages indexed.")


def main():
    conn = config.init_db()
    index_all_pages(conn)


if __name__ == "__main__":
    main()
