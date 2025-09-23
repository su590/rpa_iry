import time

from DrissionPage._pages.chromium_tab import ChromiumTab

from src.utils.logintools import Login
from src.utils.tabtools import EasyTab

def _slide(tab: ChromiumTab) -> bool:
    """
    快手广告的滑块
    """
    e_slide_tip = 'x://div[contains(text(), "向右拖动滑块填充拼图")]'
    if not tab.ele(e_slide_tip):
        return True

    # 截图、滑动
    et = EasyTab(tab)
    path = et.screenshot('c:.bg-img')
    offset = et.offset(path, '22222')
    if offset is None:
        offset = 110
    et.slide('c:.slider-btn', offset)

    # 是否刷新
    time.sleep(3)
    if tab.ele(e_slide_tip):
        return False
    return True

def _login(username: str, password: str, tab: ChromiumTab):
    """
    登录
    :param username:
    :param password:
    :param tab:
    :return:
    """
    et = EasyTab(tab)

    # 初始化
    et.get("https://agent.e.kuaishou.com/welcome?redirectUrl=%2Fdata-analysis%2Faccount-analysis")

    # 账密
    et.input("x://input[@placeholder='请输入手机号/邮箱']", username)
    et.input("x://input[@placeholder='请输入密码']", password)
    et.click("x://button[text()='快手APP账号授权登录']")
    time.sleep(1)

    # 滑块
    for _ in range(10):
        if _slide(tab):
            time.sleep(1)
            return
        time.sleep(1)
    raise TimeoutError("快手登录未能成功验证滑块")

def _is_login(tab: ChromiumTab) -> bool:
    """
    判断有没有登录
    :param tab:
    :return:
    """
    tab.get("https://agent.e.kuaishou.com/welcome?redirectUrl=%2Fdata-analysis%2Faccount-analysis")
    tab.wait.doc_loaded()
    if "redirectUrl" not in tab.url:
        return True
    else:
        return False

def _choice_account(url: str, tab: ChromiumTab) -> None:
    tab.get(url)

class KsLogin(Login):
    def __init__(self, port: int, username: str, password: str):
        super().__init__(port, username)
        self._password = password
    def _login(self, tab: ChromiumTab) -> None:
        if _is_login(tab):
            time.sleep(.5)
            return
        _login(self._username, self._password, tab)
        time.sleep(.5)

if __name__ == '__main__':
    with KsLogin(9501, "18127902005", "FDWL123456") as tab:
        pass