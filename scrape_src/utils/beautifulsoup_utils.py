import requests
from bs4 import BeautifulSoup


def get_content_from_url(url: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url).content, "html.parser")


def prettier(doc: BeautifulSoup):
    print(doc.prettify())
