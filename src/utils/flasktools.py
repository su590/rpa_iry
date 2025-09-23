# -*- coding: utf-8 -*-  
"""
@Date     : 2025-03-18
@Author   : xwq
@Desc     : <None>

"""
import re

import flask


def _camel2line(var: str) -> str:
    """
    小驼峰转下划线
    :param var:
    :return:
    """
    return re.sub(r'([a-z]|\d)([A-Z])', r'\1_\2', var).lower()


def get_c2l_dict() -> dict:
    """
    取传参json，并小驼峰转下划线
    :return:
    """
    dct: dict = flask.request.get_json()
    final_dct = {}
    for k, v in dct.items():
        final_dct[_camel2line(k)] = v
    return final_dct
