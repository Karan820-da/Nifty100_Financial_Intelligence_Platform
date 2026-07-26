def normalize_year(year):
    try:
        return str(year).strip()
        except Exception:
        return None


def normalize_ticker(ticker):
    try:
        return str(ticker).strip().upper()
        except Exception:
        return None
