from dataclasses import dataclass
from typing import Iterable
from .site_search import discover_links


@dataclass
class AuctionSource:
    url: str


def discover_auction_sources(index_url: str) -> Iterable[AuctionSource]:
    for href in discover_links(index_url, 'auction'):
        yield AuctionSource(url=href)
