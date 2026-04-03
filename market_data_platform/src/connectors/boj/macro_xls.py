from dataclasses import dataclass
from typing import Iterable


@dataclass
class MacroSource:
    code: str
    url: str


def from_config(entries: list[dict]) -> Iterable[MacroSource]:
    for item in entries:
        yield MacroSource(code=item['code'], url=item['url'])
