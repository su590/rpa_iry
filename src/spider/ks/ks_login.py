"""
这个是手机号 密码登录  也是滑块  仿照qcLogin
"""
import dataclasses
import os.path
import random

import cv2
from DrissionPage import ChromiumPage
from DrissionPage._units.actions import Actions
from DrissionPage.common import By
from PIL import Image, ImageDraw
import logging

logging.basicConfig(level=logging.INFO)


def find_all_template(im_source, im_search, threshold=0.5, maxcnt=0, rgb=False, bgremove=False):
    '''
    Locate image position with cv2.templateFind

    Use pixel match to find pictures.

    Args:
        im_source(string): 图像、素材
        im_search(string): 需要查找的图片
        threshold: 阈值，当相识度小于该阈值的时候，就忽略掉

    Returns:
        A tuple of found [(point, score), ...]

    Raises:
        IOError: when file read error
    '''
    # method = cv2.TM_CCORR_NORMED
    # method = cv2.TM_SQDIFF_NORMED
    method = cv2.TM_CCOEFF_NORMED
    DEBUG = False
    if rgb:
        s_bgr = cv2.split(im_search)  # Blue Green Red
        i_bgr = cv2.split(im_source)
        weight = (0.3, 0.3, 0.4)
        resbgr = [0, 0, 0]
        for i in range(3):  # bgr
            resbgr[i] = cv2.matchTemplate(i_bgr[i], s_bgr[i], method)
        res = resbgr[0] * weight[0] + resbgr[1] * weight[1] + resbgr[2] * weight[2]
    else:
        s_gray = cv2.cvtColor(im_search, cv2.COLOR_BGR2GRAY)
        i_gray = cv2.cvtColor(im_source, cv2.COLOR_BGR2GRAY)
        # 边界提取(来实现背景去除的功能)
        if bgremove:
            s_gray = cv2.Canny(s_gray, 100, 200)
            i_gray = cv2.Canny(i_gray, 100, 200)
            # cv2.imshow("s_gray", s_gray)
            # cv2.imshow("i_gray", i_gray)
            # cv2.waitKey(0)

        res = cv2.matchTemplate(i_gray, s_gray, method)
    w, h = im_search.shape[1], im_search.shape[0]

    result = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        if DEBUG:
            print('templmatch_value(thresh:%.1f) = %.3f' % (threshold, max_val))  # not show debug
        if max_val < threshold:
            break
        # calculator middle point
        middle_point = (top_left[0] + w / 2, top_left[1] + h / 2)
        result.append(dict(
            result=middle_point,
            rectangle=(top_left, (top_left[0], top_left[1] + h), (top_left[0] + w, top_left[1]),
                       (top_left[0] + w, top_left[1] + h)),
            confidence=max_val
        ))
        if maxcnt and len(result) >= maxcnt:
            break
        # floodfill the already found area
        cv2.floodFill(res, None, max_loc, (-1000,), max_val - threshold + 0.1, 1, flags=cv2.FLOODFILL_FIXED_RANGE)
    return result


def draw_black(path: str, w: float, h: float) -> None:
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    color = (255, 0, 0)
    draw.rectangle(
        [(0, 0), (w, h)], fill=color
    )
    image.save(path)


def img_location(big_img_path, small_img_path) -> tuple | None:
    big_img = cv2.imread(big_img_path)
    small_img = cv2.imread(small_img_path)
    result = find_all_template(im_source=big_img, im_search=small_img, threshold=0.1, maxcnt=1, rgb=False,
                               bgremove=True)
    if result:
        return (
            result[0]["result"][0], result[0]["result"][1]
        )
    return None


@dataclasses.dataclass
class info:
    name: str
    pwd: str


shop_info: dict = {
    "微医生-投放组": info("18127902005", "FDWL123456")
}


class field:
    url = "https://agent.e.kuaishou.com/welcome?redirectUrl=%2Fdata-analysis%2Faccount-analysis"
    FILE_PATH = "./pic"
    BIG_SCREEN_PNG = "big_screen.png"
    SLIDER_VERIFY = "captcha_verify.png"


class locator:
    user_input = By.XPATH, "//input[@placeholder='请输入手机号/邮箱']"  # 账号
    pwd_input = By.XPATH, "//input[@placeholder='请输入密码']"  # 密码
    agree = By.XPATH, "//input[@type='checkbox']"  # 同意协议
    login_button = By.XPATH, "//button[text()='快手APP账号授权登录']"  # 登录按钮
    slider_iframe = By.XPATH, "//iframe"  # 提示滑块验证弹框
    big_verify_img = By.XPATH, '//div[@class="image-container no-border"]'  # 待拼大图
    slider_verify_img = By.XPATH, "//img[@class='slider-img']"  # 待滑动图片
    slider_block = By.XPATH, '//i[@class="btn-icon"]'  # 滑块


class KsLogin:
    def __init__(self, page: ChromiumPage, shop_name):
        self.page = page
        self.shop_name = shop_name

    def _slider(self):
        if self.page.wait.ele_displayed(loc_or_ele=locator.slider_iframe):
            iframe = self.page.get_frame(loc_ind_ele=locator.slider_iframe)
            # 先截图大屏
            big_pic_ele = iframe.ele(locator=locator.big_verify_img)
            big_pic_ele.get_screenshot(path=field.FILE_PATH, name=field.BIG_SCREEN_PNG)
            # (宽， 高)
            big_pic_size: tuple[float, float] = big_pic_ele.rect.size
            # 再截图滑动
            slider_pic_ele = iframe.ele(locator=locator.slider_verify_img)
            slider_pic_ele.get_screenshot(path=field.FILE_PATH, name=field.SLIDER_VERIFY)
            slider_pic_size: tuple[float, float] = slider_pic_ele.rect.size
            # 将最左边的位置涂黑
            draw_black(path=f"{field.FILE_PATH}/{field.BIG_SCREEN_PNG}", w=slider_pic_size[0] + 5, h=big_pic_size[1])
            # 获取位置
            location: tuple | None = img_location(
                big_img_path=os.path.join(field.FILE_PATH, field.BIG_SCREEN_PNG),
                small_img_path=os.path.join(field.FILE_PATH, field.SLIDER_VERIFY)
            )
            if location is None:
                return False
            # 假设是左上角
            slider_pic_mid: tuple[float, float] = slider_pic_ele.rect.location
            # 终点的x,y
            slider_pic_goto: tuple[int, int] = (int(slider_pic_mid[0] + location[0]), int(slider_pic_mid[1]))
            # 拖拽
            # slider_pic_ele.drag_to(ele_or_loc=slider_pic_goto, duration=random.randint(1, 2))
            slider_block_ele = iframe.ele(locator=locator.slider_block)
            start_location: tuple[int, int] = slider_block_ele.rect.location
            print("block start location", start_location)
            print("destiny location", slider_pic_goto)
            ac = Actions(self.page)
            ac.hold(slider_block_ele)
            ac.move(offset_x=location[0] - 100, offset_y=random.randint(5, 10), duration=0.8)
            ac.right(random.randint(-3, 3))
            ac.left(3)
            self.page.wait(.5)
            ac.move(offset_x=50, offset_y=random.randint(5, 10), duration=0.5)
            self.page.wait(.5)
            ac.right(10)
            self.page.wait(.3)
            ac.right(10).release()
            # slider_block_ele.drag_to(ele_or_loc=[start_location[0] + location[0] - 14.5, start_location[1]],
            #                          duration=random.randint(1, 2))
            self.page.wait(2)

        return True

    def main(self, account_number: int):
        """
        快手登录
        :param account_number: 点击相应的代理商账户
        :return:
        """
        self.page.get(url=field.url)
        self.page.wait.load_start()
        if self.page.ele(locator=(By.XPATH, '//a[text()="进入"]')):
            self.page.ele(locator=(By.XPATH, f'//tbody/tr[{account_number}]//a[text()="进入"]')).click()  # 选择相应的代理商
            return True
        if "redirectUrl" not in self.page.url:
            return True
        # 进入登录
        account_info = shop_info[self.shop_name]
        self.page.ele(locator=locator.user_input).input(account_info.name)
        self.page.wait(1)
        self.page.ele(locator=locator.pwd_input).input(account_info.pwd)
        self.page.ele(locator=locator.login_button).click()
        self.page.wait(1, 2)
        # 进入滑块判断
        for _ in range(10):
            self.page.wait.load_start()
            logging.info(f"当前url{self.page.url}")
            if not "redirectUrl" in self.page.url:
                logging.info("已经确认登录状态")
                return True
            slider = self._slider()
            if slider is False:
                logging.info("滑动验证码失败")
        return False


if __name__ == '__main__':
    is_login = KsLogin(page=ChromiumPage(9336), shop_name="微医生-投放组").main(account_number = 1)
    print(is_login)
