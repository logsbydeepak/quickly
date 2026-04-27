from dataclasses import dataclass
from nanoid import generate

init_query = """
CREATE TABLE IF NOT EXISTS page (
    id VARCHAR(21) PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS robot (
    url TEXT PRIMARY KEY,
    content TEXT
);

CREATE TABLE IF NOT EXISTS page_link (
    from_url TEXT NOT NULL,
    to_url TEXT NOT NULL,
    PRIMARY KEY (from_url, to_url),
    FOREIGN KEY (from_url)
        REFERENCES page(url)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS word_index (
    word TEXT NOT NULL,
    page_id VARCHAR(21) NOT NULL,
    frequency INT NOT NULL,
    PRIMARY KEY (word, page_id),
    FOREIGN KEY (page_id) REFERENCES page(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_page_link_to_url ON page_link(to_url);
CREATE INDEX IF NOT EXISTS idx_page_created_at ON page(created_at);
CREATE INDEX IF NOT EXISTS idx_word_index_word ON word_index(word);
CREATE INDEX IF NOT EXISTS idx_word_index_page_id ON word_index(page_id);
"""


@dataclass
class Page:
    url: str
    title: str
    description: str
    content: str


def store_page(db, page: Page):
    id = generate()
    db.execute(
        """
        INSERT INTO page (id, url, title, description, content)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (id, page.url, page.title, page.description, page.content),
    )
    db.commit()


def retrieve_page(db, url):
    result = db.execute(
        """
        SELECT url, title, description, content FROM page
        WHERE url = %s;
        """,
        (url,),
    )

    row = result.fetchone()
    return Page(*row) if row else None


def store_robot(db, url, content):
    db.execute(
        """
        INSERT INTO robot (url, content)
        VALUES (%s, %s);
        """,
        (url, content),
    )
    db.commit()


def retrieve_robot(db, url):
    result = db.execute(
        """
        SELECT content FROM robot
        WHERE url = %s;
        """,
        (url,),
    )

    row = result.fetchone()
    return row[0] if row else None


def store_page_link(db, from_url, to_url):
    db.execute(
        """
        INSERT INTO page_link (from_url, to_url)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """,
        (from_url, to_url),
    )
    db.commit()
