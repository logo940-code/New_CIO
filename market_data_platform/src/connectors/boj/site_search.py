from typing import Iterable
from bs4 import BeautifulSoup
from src.core.http import fetch_bytes


def discover_links(index_url: str, contains: str) -> Iterable[str]:
    html = fetch_bytes(index_url).decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'lxml')
    for a in soup.select('a[href]'):
        href = a['href']
        if contains.lower() in href.lower():
            yield href
