init = """
CREATE TABLE IF NOT EXISTS quickly_page (
    id VARCHAR(21) PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS quickly_robot (
    url TEXT PRIMARY KEY,
    content TEXT
);

CREATE TABLE IF NOT EXISTS quickly_page_link (
    from_url TEXT NOT NULL,
    to_url TEXT NOT NULL,
    PRIMARY KEY (from_url, to_url),
    FOREIGN KEY (from_url)
        REFERENCES quickly_page(url)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quickly_word_index (
    word TEXT NOT NULL,
    page_id VARCHAR(21) NOT NULL,
    frequency INT NOT NULL,
    PRIMARY KEY (word, page_id),
    FOREIGN KEY (page_id) REFERENCES quickly_page(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_quickly_page_link_to_url ON quickly_page_link(to_url);
CREATE INDEX IF NOT EXISTS idx_quickly_page_created_at ON quickly_page(created_at);
CREATE INDEX IF NOT EXISTS idx_quickly_word_index_word ON quickly_word_index(word);
CREATE INDEX IF NOT EXISTS idx_quickly_word_index_page_id ON quickly_word_index(page_id);
"""

drop = """
DROP TABLE IF EXISTS quickly_word_index CASCADE;
DROP TABLE IF EXISTS quickly_page_link CASCADE;
DROP TABLE IF EXISTS quickly_robot CASCADE;
DROP TABLE IF EXISTS quickly_page CASCADE;
"""

