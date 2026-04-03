from dataclasses import dataclass


@dataclass
class RateSheetSource:
    url: str
    as_of_date: str | None = None
