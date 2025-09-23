import json
import os
from datetime import datetime
import logging
import pandas as pd
import requests
from DrissionPage import ChromiumPage

from src.service import KsAccount, PATH, JlyqAccount
from src.service.utils import send_feishu_file
from src.spider.crm import CrmIry
from src.spider.jlyq.jlyq_cost import get_cost
from src.spider.jlyq.jlyq_session import JlyqSession
from src.spider.ks.ks_cost import get_ks_cost
from src.spider.ks.ks_session import KsSession
from src.spider.ts import TsField, get_cookie, TsIry
from src.utils.pagetools import get_page


def _send_sms(time: datetime, qc_cost: float, ks_cost: float, ts_field: TsField) -> str:
    """
    弱智代码 不是我写的 懒得改了
    :param time:
    :param ts_field:
    :return:
    """
    get_time = time.now().strftime("%H:%M:%S")
    content = {
        "text":
            (f'消息推送展示项目: 微医生实时营销数据通知\n'
             f'>>获取时间: {get_time}\n'
             f'【抖音数据】\n'
             f'抖音消耗：{qc_cost}\n'
             f'【快手数据】\n'
             f'快手（申坤）消耗：{ks_cost}\n'
             f'【TS数据】\n'
             f'抖音成交（TS）：{ts_field.dy_trade}\n'
             f'抖音粉量（TS）：{ts_field.dy_fun_number}\n'
             f'快手成交（TS）：{ts_field.ks_trade}\n'
             f'快手粉量（TS）：{ts_field.ks_fun_number}\n'
             f'今日漏粉率（TS）：{ts_field.ignore_fan_rate}\n'
             )
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    msg = {
        "msg_type": "text",
        "content": content
    }
    rep = requests.request(
        method="post", headers=headers,
        url="https://open.feishu.cn/open-apis/bot/v2/hook/69268f89-834b-4280-b614-73c507c76a48",
        data=json.dumps(msg)
    )
    print(rep.json())
    print('\n')
    return rep.json()

def _get_ks_account(index: int) -> KsAccount:
    """
    从json文件当中读取出快手的账密信息
    :return:
    """
    path = os.path.join(PATH, 'ks_account.json')
    with open(path, 'r', encoding='utf-8') as f:
        account_dict: dict = json.load(f)[index]
        return KsAccount(**account_dict)

def _get_jlyq_account() -> JlyqAccount:
    """
    从json文件当中读取出巨量引擎的账密信息
    :return:
    """
    path = os.path.join(PATH, 'jlyq_account.json')
    with open(path, 'r', encoding='utf-8') as f:
        account_dict: dict = json.load(f)
        return JlyqAccount(**account_dict)

def main():
    # 拿一下ts和crm的数据
    ts_crm_page = get_page(9500)
    ts_field, ts_df = TsIry(ts_crm_page, get_cookie()).main()  # 接口获取cookie
    crm_df = CrmIry(ts_crm_page).main()
    ts_crm_page.close()

    # 拿一下巨量引擎的数据
    jlyq_account = _get_jlyq_account()
    with JlyqSession(jlyq_account.port, jlyq_account.username, jlyq_account.password) as session:
        qc_cost = get_cost(session)

    # 拿一下快手的数据
    ks_cost = 0.0
    ks_account_zero = _get_ks_account(0)
    with KsSession(ks_account_zero.port,
                   ks_account_zero.username,
                   ks_account_zero.password,
                   ks_account_zero.account_url) as session:
        ks_cost += get_ks_cost(session)
    ks_account_one = _get_ks_account(1)
    with KsSession(ks_account_one.port,
                   ks_account_one.username,
                   ks_account_one.password,
                   ks_account_one.account_url) as session:
        ks_cost += get_ks_cost(session)

    # 发送消息
    _send_sms(datetime.now(), qc_cost, ks_cost, ts_field)

    # 发送文件
    chat_id = 'oc_65fd8c5ddac0889afcb6dc20203e944d'
    file_path = os.path.join(os.path.dirname(__file__), 'iry.xlsx')

    # 1. 创建新的 xlsx
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        ts_df.to_excel(writer, sheet_name="ts_data", index=False, header=True)
        crm_df.to_excel(writer, sheet_name="crm_data", index=False, header=True)

    # 2. 发送文件
    send_feishu_file(file_path=file_path, chat_id=chat_id)

    # 3. 删除文件
    os.remove(file_path)
    logging.info("iry推送数据完成，文件已删除: %s", file_path)



if __name__ == '__main__':
    main()
