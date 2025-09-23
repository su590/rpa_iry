import json
import pandas as pd
import requests
from DrissionPage import ChromiumPage
from DrissionPage.common import By
from bs4 import BeautifulSoup
from pandas import DataFrame


class LoginInfo:
    username = 'IT-develop'
    password = 'FDAI123456'


class Website:
    url = 'https://crm.wqc.so/Datatotalcount/serviceData.html'


class Xpath:
    input_name = By.XPATH, '//input[@name="username"]'  # 输入用户名
    input_password = By.XPATH, '//input[@name="password"]'  # 输入密码
    click_to_login = By.XPATH, '//button[@class="loginBtn"]'  # 点击登录


class CrmIry:
    def __init__(self, page: ChromiumPage):
        self.page = page

    def login(self):
        self.page.wait.ele_displayed(Xpath.input_name, timeout=5)

        self.page.ele(locator=Xpath.input_name).click()
        self.page.ele(locator=Xpath.input_name).input(LoginInfo.username)

        self.page.ele(locator=Xpath.input_password).click()
        self.page.ele(locator=Xpath.input_password).input(LoginInfo.password)

        self.page.ele(locator=Xpath.click_to_login).click()
        self.page.wait(5)
        return

    def get_form(self) -> DataFrame:  # 从网页上读取表格
        self.page.get(Website.url)
        self.page.wait(5)
        print(self.page.url)
        if self.page.url.find("serviceData") == -1:  # 根据url判断是否需要登录
            self.login()
            self.page.get(Website.url)
            self.page.wait(2)
        soup = BeautifulSoup(self.page.html, 'html.parser')
        tables = soup.find_all('table')
        print(tables[0])
        table = tables[0]
        rows = table.find_all('tr')
        row_head = table.find('thead').find_all('tr')  # 获取表格的标题行

        data = []
        header = []

        # 获取标题行的文本
        for row in row_head:
            cols = row.find_all('th')
            header = [ele.text.strip() for ele in cols]

        # 获取数据行的文本
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # 去除空值

        df = pd.DataFrame(data, columns=header)  # 设置DataFrame的列名为表格的标题行
        df = df.drop(0)  # 删除第一行空行
        print(df.head())
        return df

    def main(self):
        return self.get_form()


if __name__ == '__main__':
    df = CrmIry(ChromiumPage()).main()
    df.to_excel(r'C:\Users\Administrator\Desktop\test621.xlsx', index=False)
    print(df.to_string(index=False))
    content = {
        "text":
            (f'{df.to_string(index=False)}'
             )
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    msg = {
        "msg_type": "text",
        "content": content
    }
    rep = requests.request(
        method="post", headers=headers,
        url="https://open.feishu.cn/open-apis/bot/v2/hook/3b4180bb-2719-434c-ab71-ad51f44bee22", data=json.dumps(msg)
    )
