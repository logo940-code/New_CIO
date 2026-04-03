from dataclasses import dataclass
from datetime import date


@dataclass
class QCCheck:
    rule_name: str
    passed: bool
    severity: str
    message: str


def check_date_order(issue_date, maturity_date) -> QCCheck:
    if issue_date and maturity_date and maturity_date <= issue_date:
        return QCCheck('maturity_after_issue', False, 'error', 'maturity_date must be after issue_date')
    return QCCheck('maturity_after_issue', True, 'info', 'ok')


def check_non_negative(name: str, value) -> QCCheck:
    if value is not None and value < 0:
        return QCCheck(f'{name}_non_negative', False, 'error', f'{name} must be non-negative')
    return QCCheck(f'{name}_non_negative', True, 'info', 'ok')


def check_not_future(name: str, value, as_of: date) -> QCCheck:
    if value and value > as_of:
        return QCCheck(f'{name}_not_future', False, 'warning', f'{name} is after ingestion date')
    return QCCheck(f'{name}_not_future', True, 'info', 'ok')
