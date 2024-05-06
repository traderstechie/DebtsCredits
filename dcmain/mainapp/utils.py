import os
from decimal import Decimal

from flask import current_app

from dcmain.config import Config
from dcmain.appstrings import ccl, lcl, ucl


def is_eq(v1, v2):
    return v1 == v2


def not_eq(v1, v2):
    return v1 != v2


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
    # if isinstance(value, str):
    #     value = Decimal(value)
    return format_decimal(value, places=2, currency_symbol=currency_symbol, rd=rd)


TEST_DCP_PARAMS = {
    lcl.development: {
        lcl.user_id: "1088823636",
        lcl.dc_profile_id: "3505DCP36219811",
        lcl.pin: os.environ.get(ucl.TP_DEV_PIN),
        lcl.password: os.environ.get(ucl.TP_DEV_PASSWORD),
    },
    lcl.production: {
        lcl.pin: "",
        lcl.password: "test1234",
        lcl.user_id: "1045236820",
        lcl.dc_profile_id: "4103DCP20256990",
    },
}


def get_route_essentials(headers: dict = None):
    if current_app.config.get(ucl.PRODUCTION_ENV):
        d = TEST_DCP_PARAMS[lcl.production]

        root_domain = "https://tradepally.com"

        headers.update(
            {ccl.AUTHORIZATION: Config.TRADEPALLY_PRODUCTION_API_AUTH_TOKEN})
    else:
        d = TEST_DCP_PARAMS[lcl.development]

        root_domain = "http://localhost:5000"

        headers.update(
            {ccl.AUTHORIZATION: Config.TRADEPALLY_LOCALHOST_API_AUTH_TOKEN})

    return {
        lcl.params: d,
        lcl.headers: headers,
        lcl.root_domain: root_domain
    }
