from decimal import Decimal


def is_valid_numeric(string, not_zero=False, not_fraction=False, not_negative=False):
    """
    Check that a string is numeric  (eg: 123, -123, 123.0)
    :param string:
    :param not_zero: if not_zero=True, return False if string is 0 or 0.0 or 0.0zeroes
    :param not_fraction: if not_fraction=True, return False if string has "." (ie: is fractional)
    :param not_negative:  if not_negative=True, return False if string has "-" (ie: is negative)
    :return:
    """
    if string == '':
        return False
    if not_zero:
        if string.isnumeric() and Decimal(string) == 0:
            return False
        elif ('.' in string) and string.replace('.', '').isnumeric() and Decimal(string) == 0:
            return False
    if not_fraction and ('.' in string):
        return False
    if not_negative and ('-' in string):
        return False
    # Else
    return string.isnumeric() or (string[0] == "-" and string[1:].isalnum()) or string.replace('.', '').isnumeric()


def format_decimal(value, places=2, currency_symbol=None, no_grouping=False, rd=False):
    """
    :param value: Can be Decimal/int/float/str. (str should pass ``is_valid_numeric`` check). 
        Any other obj type aside the ones specified for `value` above will fail
    :param places:
    :param currency_symbol:
    :param no_grouping:
    :param rd: if True, a Decimal obj will be returned after applying specified formatting
    :return:
    """
    if isinstance(value, (Decimal, int, float)):
        raw_deci = Decimal(format(value, f".{places}f"))
    elif isinstance(value, str) and is_valid_numeric(value):
        raw_deci = Decimal(format(Decimal(value), f".{places}f"))
    else:
        raise ValueError(
            f"Expected one of (Decimal, int, float, str), not {type(value)}")

    if rd:
        return raw_deci
    elif no_grouping:
        grouped_deci = raw_deci
    else:
        grouped_deci = f"{raw_deci:,}"

    if currency_symbol:
        if raw_deci < 0:
            return f"-{currency_symbol}{grouped_deci[1:]}"
        return f"{currency_symbol}{grouped_deci}"

    return grouped_deci


def two_decimals(value, currency_symbol=None, rd=False):
    """See `format_decimal` function for modalities"""
    return format_decimal(value, places=2, currency_symbol=currency_symbol, rd=rd)
