import utils
import db_utils


def spider(url):
    db_page = db_utils.retrieve_page(url)

    if db_page:
        print(f"Found cached page for {url}")
        print(f"Title: {db_page.title}")
        print(f"Description: {db_page.description}")
        print(f"Body: {db_page.content}")
        return

    robots_txt = None

    p = utils.urlparse(url)
    robots_url = f"{p.scheme}://{p.netloc}/robots.txt"

    db_res = db_utils.retrieve_robot(robots_url)
    if db_res:
        print(f"Found cached robots.txt for {url}")
        robots_txt = db_res
    else:
        print(f"Fetching robots.txt for {url}")
        robots_txt = utils.fetch(robots_url)
        if robots_txt:
            db_utils.store_robot(robots_url, robots_txt)

    if robots_txt is None:
        print(f"Could not fetch robots.txt for {url}")
        return

    if not utils.check_is_allowed(robots_txt, url):
        print(f"Access to {url} is disallowed by robots.txt")
        return

    soup = utils.crawl(url)
    if soup is None:
        print(f"Failed to crawl {url}")
        return

    title = utils.get_title(soup)
    description = utils.get_description(soup)
    body = utils.get_body(soup)
    links = utils.extract_links(soup, url)

    page = db_utils.Page(url=url, title=title, description=description, content=body)
    db_utils.store_page(page)

    for link in links:
        db_utils.store_page_link(url, link)

    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Body: {body}")


def main():
    spider("https://pypi.org/project/beautifulsoup4/")
    spider("https://en.wikipedia.org/wiki/JavaScript")


if __name__ == "__main__":
    main()
