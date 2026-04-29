from dataclasses import dataclass
from nanoid import generate
from db import get_db


@dataclass
class Page:
    url: str
    title: str
    description: str
    content: str


def store_page(page: Page):
    db = get_db()

    id = generate()
    db.execute(
        """
        INSERT INTO quickly_page (id, url, title, description, content)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (id, page.url, page.title, page.description, page.content),
    )
    db.commit()


def retrieve_page(url):
    db = get_db()
    result = db.execute(
        """
        SELECT url, title, description, content FROM quickly_page
        WHERE url = %s;
        """,
        (url,),
    )

    row = result.fetchone()
    return Page(*row) if row else None


def store_robot(url, content):
    db = get_db()
    db.execute(
        """
        INSERT INTO quickly_robot (url, content)
        VALUES (%s, %s);
        """,
        (url, content),
    )
    db.commit()


def retrieve_robot(url):
    db = get_db()
    result = db.execute(
        """
        SELECT content FROM quickly_robot
        WHERE url = %s;
        """,
        (url,),
    )

    row = result.fetchone()
    return row[0] if row else None


def store_page_link(from_url, to_url):
    db = get_db()
    db.execute(
        """
        INSERT INTO quickly_page_link (from_url, to_url)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """,
        (from_url, to_url),
    )
    db.commit()
