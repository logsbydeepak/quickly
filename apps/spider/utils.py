from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from urllib.robotparser import RobotFileParser
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}


def fetch(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def check_is_allowed(robots_text, url):
    rp = RobotFileParser()
    rp.parse(robots_text.splitlines())

    return rp.can_fetch(headers["User-Agent"], url)


def crawl(url):
    html = fetch(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, "html.parser")
    return soup


def _clean(text):
    return text.replace("\x00", "") if text else text


def get_title(soup):
    title = soup.title.string if soup.title else None
    title = _clean(title)
    return title if title and len(title.strip()) > 0 else None


def get_description(soup):
    description_tag = soup.find("meta", attrs={"name": "description"})
    if description_tag and "content" in description_tag.attrs:
        return _clean(description_tag["content"].strip())
    return None


def get_body(soup):
    body = soup.body

    if not body:
        return ""

    text = body.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)

    return _clean(text)


def extract_links(soup, base_url):
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()

        if href.startswith(("javascript:", "mailto:", "tel:")):
            continue

        full_url = urljoin(base_url, href)
        full_url, _ = urldefrag(full_url)

        if full_url.startswith(("http://", "https://")):
            links.add(full_url)

    return list(links)
