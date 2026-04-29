import re
from pathlib import Path

import nltk
from nltk.corpus import stopwords


NLTK_DATA_DIR = Path("/tmp/nltk_data")
NLTK_DATA_DIR.mkdir(parents=True, exist_ok=True)
nltk.data.path.append(str(NLTK_DATA_DIR))

try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", download_dir=str(NLTK_DATA_DIR), quiet=True)
    STOP_WORDS = set(stopwords.words("english"))


def tokenize(text):
    if not text:
        return []

    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]
