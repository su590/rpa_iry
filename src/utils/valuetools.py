# -*- coding: utf-8 -*-  
"""
@Date     : 2025-02-20
@Author   : xwq
@Desc     : <None>

"""
import decimal


def dcml(v: str | float | int | decimal.Decimal) -> decimal.Decimal:
    if isinstance(v, decimal.Decimal):
        return v
    if v is None:
        return decimal.Decimal(0)
    v = str(v).strip()
    v = v.replace(',', '')
    if v in ('-', ''):
        return decimal.Decimal(0)
    if v[-1] == '万':
        v = decimal.Decimal(v[:-1]) * decimal.Decimal(10000)
    elif v[-1] == '%':
        v = decimal.Decimal(v[:-1]) / decimal.Decimal(100)
    return decimal.Decimal(v)


def get_decimal(jsn: dict, *keys: str | int) -> decimal.Decimal:
    try:
        result: dict | str | float | int = jsn
        for key in keys:
            result = result[key]
        if result is None:
            return dcml(0)
        return dcml(result)
    except (KeyError, IndexError):
        return dcml(0)


gd = get_decimal
