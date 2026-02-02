from urllib.request import urlopen

from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString


def _fetch_url_content(url: str) -> BeautifulSoup | None:
    try:
        response = urlopen(url)
        html_content = response.read().decode("utf-8")
        return BeautifulSoup(html_content, "html.parser")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_all_links(url: str) -> ResultSet[PageElement | Tag | NavigableString] | None:
    if url_content := _fetch_url_content(url):
        if all_links := url_content.find_all("a"):
            return all_links
    raise ValueError(f"No links found for url={url}")
