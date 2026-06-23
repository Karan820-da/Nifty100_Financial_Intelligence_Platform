def normalize_year(year):
    try:
        return str(year).strip()
    except:
        return None


def normalize_ticker(ticker):
    try:
        return str(ticker).strip().upper()
    except:
        return None