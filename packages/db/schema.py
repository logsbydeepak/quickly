init = """
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

drop = """
DROP TABLE IF EXISTS word_index CASCADE;
DROP TABLE IF EXISTS page_link CASCADE;
DROP TABLE IF EXISTS robot CASCADE;
DROP TABLE IF EXISTS page CASCADE;
"""
