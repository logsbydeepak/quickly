from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}


def spider(url):
    robots_txt = fetch_robots_txt(url)
    if robots_txt is None:
        print(f"Could not fetch robots.txt for {url}")
        return

    if not check_is_allowed(robots_txt, url):
        print(f"Access to {url} is disallowed by robots.txt")
        return

    soup = crawl(url)
    if soup is None:
        print(f"Failed to crawl {url}")
        return

    print(
        soup.prettify()[:500]
    )  # Print the first 500 characters of the prettified HTML

    title = get_title(soup)
    description = get_description(soup)
    body = get_body(soup)

    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Body: {body}")


def fetch(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_robots_txt(url):
    p = urlparse(url)
    robots_url = f"{p.scheme}://{p.netloc}/robots.txt"
    return fetch(robots_url)


def check_is_allowed(robots_text, url):
    rp = RobotFileParser()
    rp.parse(robots_text.splitlines())

    return rp.can_fetch(headers["User-Agent"], url)


def crawl(url):
    html = fetch(url)
    if html is None:
        return []

    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_title(soup):
    title = soup.title.string
    return title if title and len(title.strip()) > 0 else None


def get_links(soup, base_url):
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/"):
            href = base_url + href
        elif not href.startswith("http"):
            continue
        links.append(href)
    return links


def get_description(soup):
    description_tag = soup.find("meta", attrs={"name": "description"})
    if description_tag and "content" in description_tag.attrs:
        return description_tag["content"].strip()
    return None


def get_body(soup):
    body = soup.body

    if not body:
        return ""

    text = body.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)

    return text
