import pandas as pd


def read_excel_sheets(path: str) -> dict[str, pd.DataFrame]:
    xls = pd.ExcelFile(path)
    return {sheet: pd.read_excel(path, sheet_name=sheet) for sheet in xls.sheet_names}
