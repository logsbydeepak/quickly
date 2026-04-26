import config
import spider


def main():
    config.init_db()
    spider.spider("https://pypi.org/project/beautifulsoup4/")

    # config.init_redis()


if __name__ == "__main__":
    main()
