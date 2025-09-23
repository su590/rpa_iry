import dataclasses
import os
import re
from datetime import datetime

import pandas as pd
import requests
from DrissionPage import ChromiumPage
from DrissionPage.common import By
from bs4 import BeautifulSoup
from pandas import DataFrame


@dataclasses.dataclass
class TsField:
    dy_trade: float  # 抖音成交(TS)
    dy_fun_number: int  # 抖音粉量(TS)
    ks_trade: float  # 快手成交(TS)
    ks_fun_number: int  # 快手粉量(TS)
    ignore_fan_rate: str  # 今日漏粉率(TS)


def get_cookie() -> str:
    url = "https://link.wqc.so/Member/signupRpa"
    data = {"username": "fandow", "password": 'fandow654321'}
    token: str = requests.post(url, data=data).json()["data"]["token"]
    return f"PHPSESSID={token}"

def get_whole_download_excel_api():
    today = datetime.today().strftime('%Y-%m-%d')
    print("download_file time param： ", today)
    download_excel_api = (f"https://link.wqc.so/Autoconvertfans/exportAdMessage.html?linkName=&groupNameId=&groupName=&"
                          f"service=&beginDate={today}&endDate={today}&chooseBeginDate=&chooseEndDate=&ident=")
    return download_excel_api


class Website:
    url = 'https://link.wqc.so/Autoconvertfans/index.html'


class XPath:
    # stats_link = By.XPATH, "//a[text()='统计链接']"  # hover
    # auto_fan_system = By.XPATH, "//a[text()='自动转粉系统']"
    export_excel = By.XPATH, "//input[@value='导出表格']"  # 导出表格
    ignore_fan_rate = By.XPATH, '//td[text()="汇总"]/following-sibling::td'  # 漏粉率 3 of 13

    refresh_button = By.XPATH, "//button[@class='btn success'][text()='刷新']"  # 刷新 2 of 4
    branch_business_form = By.XPATH, "//div[@id='salesDataTb']//table[@class='dash_table zebra-striped']"  # 判断刷新出表格没


class Caculator:
    def __init__(self, df: DataFrame):
        self.df = df

    def get_dy_trade(self) -> float:
        df = self.df

        df = df[~df['链接名称'].str.contains('快手')]  # 删除包括快手的行
        dy_trade = df['新粉销售额'].sum()
        return dy_trade

    def get_dy_fun_number(self) -> int:
        df = self.df

        df = df[~df['链接名称'].str.contains('快手')]  # 删除包括快手的行
        dy_fun_number = df['新增粉丝数'].sum()
        return dy_fun_number

    def get_ks_trade(self) -> float:
        df = self.df

        df = df[df['链接名称'].str.contains('快手')]  # 删除包括快手的行
        ks_trade = df['新粉销售额'].sum()
        return ks_trade

    def get_ks_fun_number(self) -> int:
        df = self.df

        df = df[df['链接名称'].str.contains('快手')]  # 删除包括快手的行
        ks_fun_number = df['新增粉丝数'].sum()
        return ks_fun_number


class TsIry:
    def __init__(self, page: ChromiumPage, cookie: str):
        self.page = page
        self.cookie = cookie
        cookies = f'domain=link.wqc.so; {cookie}'
        print("cookies:", cookies)
        self.page.set.cookies(cookies)  # 把接口获取的cookie填进去
        self.page.wait(5)
        self.page.get('https://link.wqc.so/Autoconvertfans/index.html')

    def get_ignore_fan_rate(self) -> str:  # 接口方式 拿到漏粉率
        url = Website.url

        headers = {
            'cookie': self.cookie
        }
        response = requests.get(url, headers=headers).text
        pattern = r'<td class="align-center">汇总</td>(.*?)<!--今日总粉丝数-->(.*?)<!--每五分钟标准进粉数-->'
        result = re.findall(pattern, response, re.DOTALL)
        for group in result:
            values = re.findall(r'<td.*?>(.*?)</td>', group[1], re.DOTALL)
            print(values[-1])
            return values[-1]  # 从页面html中解析除需要的字段 只有一个匹配的

    def get_branch_business_form(self) -> DataFrame:  # 分部营业数据表
        self.page.get(Website.url)
        self.page.wait(5)

        self.page.wait.ele_displayed(loc_or_ele=XPath.refresh_button, timeout=10)
        self.page.ele(locator=XPath.refresh_button, index=2).click()

        self.page.wait.ele_displayed(loc_or_ele=XPath.branch_business_form, timeout=10)
        soup = BeautifulSoup(self.page.html, 'html.parser')
        tables = soup.find_all('table')
        # print(tables[0])
        table = tables[-1]  # 刷新出来的 最下面的table
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

    def get_file(self) -> str:  # 接口方式下载表格
        url = get_whole_download_excel_api()
        headers = {
            'cookie': self.cookie,
        }
        response = requests.get(url, headers=headers)
        new_filename = 'newnew.xlsx'  # 重命名后的文件名
        download_directory = r'./'  # 自定义的下载目录路径
        if response.status_code == 200:
            file_path = os.path.join(download_directory, new_filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print('文件下载成功并重命名为', file_path)
            return file_path
        else:
            print('文件下载失败')
            return '文件下载失败'

    def parse(self) -> tuple[DataFrame, str]:  # 接口方式 拿到df和漏粉率
        ignore_fan_rate = self.get_ignore_fan_rate()
        file = self.get_file()
        df = pd.read_excel(file)
        self.page.wait(3)
        os.remove(file)  # 读取之后删除
        print(df.head())
        return df, ignore_fan_rate  # 返回不含路径和后缀的文件名

    def get_data(self) -> tuple[TsField, DataFrame]:
        df, ignore_fan_rate = self.parse()

        dy_trade = Caculator(df).get_dy_trade()
        ks_trade = Caculator(df).get_ks_trade()
        ks_fun_number = Caculator(df).get_ks_fun_number()
        dy_fun_number = Caculator(df).get_dy_fun_number()

        ts_field = TsField(dy_trade=dy_trade, ks_trade=ks_trade,
                           dy_fun_number=dy_fun_number, ks_fun_number=ks_fun_number,
                           ignore_fan_rate=ignore_fan_rate)
        df: DataFrame = self.get_branch_business_form()

        return ts_field, df

    def main(self):
        return self.get_data()


if __name__ == '__main__':
    print(TsIry(ChromiumPage(), get_cookie()).get_data())
