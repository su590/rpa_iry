# -*- coding: utf-8 -*-  
"""
@Date     : 2025-02-20
@Author   : xwq
@Desc     : <None>

"""
import uuid

from src.rds import REDIS

_PREFIX = 'timeframe:flag'


class Flag:
    def __init__(self, id_: str = None, ):
        if id_ is None:
            id_ = str(uuid.uuid4())
        id_ = id_.replace(':', '-')
        self._id: str = id_

    @property
    def id(self) -> str:
        return self._id

    def save(self, timeout: int = None) -> bool:
        if timeout is None:
            result = REDIS.set(f'{_PREFIX}:{self._id}', self._id, nx=True)
        else:
            result = REDIS.set(f'{_PREFIX}:{self._id}', self._id, ex=timeout, nx=True)
        return result is True

    def exist(self) -> bool:
        return REDIS.get(f'{_PREFIX}:{self._id}') is not None

    def delete(self):
        REDIS.delete(f'{_PREFIX}:{self._id}')

    def ttl_hms(self) -> str | None:
        """
        获取当前key的剩余过期时间（格式化为 HH:MM:SS)
        :return: str（格式化后的时间），如果没有设置过期使劲啊返回None
        """
        ttl_seconds = REDIS.ttl(f"{_PREFIX}:{self._id}")
        if ttl_seconds is None or ttl_seconds < 0:
            # -1表示永不过期，-2表示key不存在
            return None
        hours, remainder = divmod(ttl_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"


    @classmethod
    def clear(cls):
        key = f'{_PREFIX}:*'
        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = REDIS.scan(cursor, match=key)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        for k in keys:
            REDIS.delete(k)


Flag.clear()

