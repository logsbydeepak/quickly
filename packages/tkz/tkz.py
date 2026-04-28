import re

import nltk
from nltk.corpus import stopwords


nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))


def tokenize(text):
    if not text:
        return []

    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]
