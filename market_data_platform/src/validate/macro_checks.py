from .rules import QCCheck


def validate_macro_row(row: dict) -> list[QCCheck]:
    checks = []
    if row.get('value') is None:
        checks.append(QCCheck('macro_value_not_null', False, 'warning', 'macro value is null'))
    else:
        checks.append(QCCheck('macro_value_not_null', True, 'info', 'ok'))
    return checks
