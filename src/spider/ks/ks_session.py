import time

import requests

from src.spider.ks.ks_cost import check
from src.spider.ks.ks_login_new_version import KsLogin
from src.utils.logintools import Session
from src.utils.tabtools import EasyTab


class KsSession(Session):
    def __init__(self, port: int, username: str, password: str, account_url: str):
        super().__init__(port, username)
        self._password = password
        self._account_url = account_url

    def _check(self, session: requests.Session):
        check(session)

    def _session(self) -> requests.Session:
        with KsLogin(self._port, self._username, self._password) as tab:
            time.sleep(1)
            return EasyTab(tab).session(self._account_url)