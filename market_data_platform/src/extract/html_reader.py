from bs4 import BeautifulSoup


def to_text(html: str) -> str:
    return BeautifulSoup(html, 'lxml').get_text('
')
