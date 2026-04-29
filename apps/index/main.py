from collections import Counter
from db import get_db
import tkz

insert_query = """
INSERT INTO quickly_word_index(word, page_id, frequency)
VALUES (%s, %s, %s)
ON CONFLICT (word, page_id)
DO UPDATE SET frequency = EXCLUDED.frequency
"""


def index_page(page_id, title="", description="", content=""):
    counts = Counter()

    for word in tkz.tokenize(title):
        counts[word] += 5

    for word in tkz.tokenize(description):
        counts[word] += 3

    for word in tkz.tokenize(content):
        counts[word] += 1

    rows = [(word, page_id, freq) for word, freq in counts.items()]

    if not rows:
        return

    db = get_db()

    with db.cursor() as cur:
        cur.executemany(insert_query, rows)

    db.commit()


select_query = """
SELECT p.id, p.title, p.description, p.content
FROM quickly_page p
WHERE NOT EXISTS (
    SELECT 1
    FROM quickly_word_index w
    WHERE w.page_id = p.id
)
LIMIT %s;
"""


def index_all_pages(batch_size=10):
    total = 0

    db = get_db()

    while True:
        rows = db.execute(select_query, (batch_size,)).fetchall()

        if not rows:
            break

        for page_id, title, description, content in rows:
            index_page(page_id, title, description, content)

        db.commit()

        total += len(rows)
        print(f"Indexed {total} pages")

    print("All pages indexed.")
