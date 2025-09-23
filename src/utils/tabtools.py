# -*- coding: utf-8 -*-  
"""
@Date     : 2025-02-20
@Author   : xwq
@Desc     : <None>

"""
import base64
import logging
import os
import random
import time

import requests
from DrissionPage.items import ChromiumFrame, ChromiumTab

from src import get_config
from src.config import COMMON_DOWNLOAD_PATH
from src.utils.dsptools import dsptools


class EasyTab:
    def __init__(self, tab: ChromiumTab | ChromiumFrame):
        self._tab = tab

    def get(self, url: str):
        tab = self._tab
        tab.wait.doc_loaded()
        if tab.url.rstrip('/') != url:
            tab.get(url)
            tab.wait.doc_loaded()

    def click(self, ele: str, pierce: bool = False):
        tab = self._tab
        tab.wait.ele_displayed(ele, raise_err=True, timeout=10)
        time.sleep(random.uniform(0.2, 0.3))
        if pierce and tab.ele(ele).states.is_covered:
            dsptools.pierce(tab, ele)
            time.sleep(.5)
        tab.actions.move_to(self.point(ele)).click()

    def wait(self, ele: str, timeout: int = 10, raise_err: bool = True):
        tab = self._tab
        tab.wait.eles_loaded(ele, raise_err=raise_err, timeout=timeout)
        tab.wait.ele_displayed(ele, raise_err=raise_err, timeout=timeout)

    def input(self, ele: str, text: str):
        self.click(ele)
        dsptools.backspace(self._tab, ele)
        dsptools.typewrite(self._tab, ele, text)

    def screenshot(self, ele: str) -> str:
        tab = self._tab
        tab.wait.ele_displayed(ele, raise_err=True, timeout=10)
        time.sleep(.5)
        path = os.path.join(COMMON_DOWNLOAD_PATH,
                            f'img_{int(time.time() * 1000)}_{int(random.random() * 1000)}.png')
        tab.ele(ele).get_screenshot(path)
        return path

    def location(self, ele: str) -> tuple[int, int]:
        tab = self._tab
        tab.wait.ele_displayed(ele, raise_err=True, timeout=10)
        x = tab.ele(ele).rect.location
        return int(x[0]), int(x[1])

    def size(self, ele: str) -> tuple[int, int]:
        tab = self._tab
        tab.wait.ele_displayed(ele, raise_err=True, timeout=10)
        s = tab.ele(ele).rect.size
        return int(s[0]), int(s[1])

    def point(self, ele: str) -> tuple[int, int]:
        x, y = self.location(ele)
        w, h = self.size(ele)
        return x + w // 2, y + h // 2

    @classmethod
    def offset(cls, img: str, typ: str) -> int | None:
        """
        识别图片应滑动距离
        :param img: 图片地址
        :param typ: 云码类型, 如"22222"
        """
        with open(img, 'rb') as f:
            b = base64.b64encode(f.read()).decode()
        response = requests.post(
            url='https://api.jfbym.com/api/YmServer/customApi',
            headers={'Content-Type': 'application/json'},
            json={
                "token": get_config('ym', 'token'),
                "type": typ,
                "image": b,
            }
        )
        jsn = response.json()
        if jsn['code'] != 10000:
            logging.error(f'云码平台响应错误: {jsn}')
            return None
        return int(jsn['data']['data'])

    @classmethod
    def add(cls, a: tuple[float, float], b: tuple[float, float]) -> tuple[int, int]:
        return int(a[0] + b[0]), int(a[1] + b[1])

    def slide(
            self,
            ele: str,
            offset: int,
            y_scope: int = None,
            x_scope: float = 0.3,
            duration: float = 1.5
    ):
        """
        模拟人类拖动滑块，带补偿 / 抖动 / 加速度曲线
        """
        if y_scope is None:
            y_scope = self.size(ele)[1]
        y_scope //= 2

        # ---- offset 补偿（保留你的逻辑）----
        x_scope = self.size(ele)[0]
        offset -= (x_scope + 20)

        duration = max(1.5, duration)
        start = self.point(ele)

        ac = self._tab.actions
        ac.move_to(start).hold()

        # ---- y 抖动逻辑 ----
        def with_jitter(x, base_y=0):
            return (x, base_y + random.randint(-3, 3))

        # ---- 轨迹生成（加速度曲线：先快后慢）----
        steps = [0.2, 0.5, 0.8, 1.0]  # 占比：20% → 50% → 80% → 100%
        times = [0.2, 0.3, 0.3, 0.2]  # 时间占比

        last_x = 0
        for i, step in enumerate(steps):
            x = offset * step
            t = duration * times[i]
            ac.move_to(self.add(start, with_jitter(x, 0)), t)
            last_x = x

        ac.release()

    def session(self, url: str = None, all_info: bool = None, all_domains: bool = None) -> requests.Session:
        if url is not None:
            self.get(url)
        kwargs = {}
        if all_info is not None:
            kwargs['all_info'] = all_info
        if all_domains is not None:
            kwargs['all_domains'] = all_domains
        cookies = {x['name']: x['value'] for x in self._tab.cookies(**kwargs)}
        session = requests.session()
        session.cookies.update(cookies)
        return session

    def catch(self, ele: str, url: str) -> dict:
        """
        抓取: 点击, 并监听某个报文响应
        """
        tab = self._tab
        tab.listen.start(url)
        self.click(ele)
        dp = tab.listen.wait(timeout=10, raise_err=True)
        body = dp.response.body
        tab.listen.stop()
        return body
