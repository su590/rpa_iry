# -*- coding: utf-8 -*-  
"""
@Date     : 2025-02-20
@Author   : xwq
@Desc     : <None>

"""

import redis

from src.config import get_config


def _client():
    """
    获取redis连接
    :return:
    """
    conf = get_config('redis')
    r = redis.Redis(
        host=conf['host'],
        port=conf['port'],
        password=conf['password'],
        db=conf['db'],
    )
    return r


REDIS = _client()
