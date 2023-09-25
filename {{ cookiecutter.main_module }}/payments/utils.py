import pycountry


def get_all_currencies_code():
    currencies_code = []
    for currency in pycountry.currencies:
        currencies_code.append((currency.alpha_3, f"{currency.name}"))
    return currencies_code
