from collections import deque
import sys
import time

import utils
import db_utils


def crawl_one(url):
    """Fetch a fresh URL and store it. Returns (links, None) or (None, reason)."""
    p = utils.urlparse(url)
    robots_url = f"{p.scheme}://{p.netloc}/robots.txt"

    robots_txt = db_utils.retrieve_robot(robots_url)
    if robots_txt is None:
        robots_txt = utils.fetch(robots_url)
        if robots_txt is not None:
            db_utils.store_robot(robots_url, robots_txt)

    if robots_txt is None:
        return None, "no robots.txt"

    if not utils.check_is_allowed(robots_txt, url):
        return None, "disallowed by robots.txt"

    soup = utils.crawl(url)
    if soup is None:
        return None, "fetch failed"

    title = utils.get_title(soup)
    if title is None:
        return None, "no title"

    description = utils.get_description(soup)
    body = utils.get_body(soup)
    links = utils.extract_links(soup, url)

    page = db_utils.Page(url=url, title=title, description=description, content=body)
    db_utils.store_page(page)
    db_utils.store_page_links(url, links)

    return links, None


def crawl(seeds, max_pages=50, delay=1.0):
    """BFS crawl from seed URLs, capped at max_pages newly fetched pages."""
    frontier = deque(seeds)
    visited = set()
    fetched = 0

    while frontier and fetched < max_pages:
        url = frontier.popleft()
        if url in visited:
            continue
        visited.add(url)

        if db_utils.retrieve_page(url):
            links = db_utils.get_outgoing_links(url)
            print(f"        cache  {url} ({len(links)} links)")
        else:
            links, reason = crawl_one(url)
            if links is None:
                print(f"        skip   {url} ({reason})")
                continue
            fetched += 1
            print(f"[{fetched}/{max_pages}] fetch  {url} ({len(links)} links)")
            time.sleep(delay)

        for link in links:
            if link not in visited:
                frontier.append(link)

    print(f"\nDone. Fetched {fetched} new pages, visited {len(visited)} URLs.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url> [url ...]")
        sys.exit(1)
    for seed in sys.argv[1:]:
        print(f"\n=== Crawl from {seed} ===")
        crawl([seed], max_pages=50, delay=1.0)


if __name__ == "__main__":
    main()
