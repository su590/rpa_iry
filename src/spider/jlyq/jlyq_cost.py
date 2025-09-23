import datetime
import logging

import requests
import json

def get_cost(session: requests.Session) -> float:
  """
  拿一下抖音广告消息
  :param session: session
  :return: 获取到的广告消耗
  """
  url = "https://business.oceanengine.com/bp/api/promotion/promotion_common/get_overview_data"
  start_time = int(datetime.datetime.combine(datetime.date.today(), datetime.time().min).timestamp())
  end_time = int(datetime.datetime.combine(datetime.date.today(), datetime.time().max).timestamp())
  payload = json.dumps({
    "startTime": f"{start_time}",
    "endTime": f"{end_time}",
    "fields": [
      "stat_cost",
      "show_cnt",
      "convert_cnt",
      "conversion_cost",
      "conversion_rate",
      "cpm_platform"
    ],
    "appKey": 0,
    "queryDimensions": 1,
    "filters": {
      "campaignType": 0,
      "advType": 2
    },
    "extraRefer": {
      "pageId": "7363497363769507890",
      "moduleId": "7346249523100090378",
      "dataKey": "bp_promotion_chart_ad_bidding"
    },
    "isActive": True
  })
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://business.oceanengine.com',
    'priority': 'u=1, i',
    'referer': 'https://business.oceanengine.com/site/account-manage/ad/bidding/superior/account',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  }

  response = session.request("POST", url, headers=headers, data=payload)
  response_json = response.json()
  cost = response_json['data']['list'][0]['total']
  logging.info(f"抖音下获取到的消耗是{cost}")
  return cost

def check_session(session: requests.Session):
  """
  测试一下session
  测试通过的话就可以直接从redis当中拿session
  :param session:
  :return:
  """
  url = "https://business.oceanengine.com/bp/api/promotion/promotion_common/get_overview_data"
  start_time = int(datetime.datetime.combine(datetime.date.today(), datetime.time().min).timestamp())
  end_time = int(datetime.datetime.combine(datetime.date.today(), datetime.time().max).timestamp())
  payload = json.dumps({
    "startTime": f"{start_time}",
    "endTime": f"{end_time}",
    "fields": [
      "stat_cost",
      "show_cnt",
      "convert_cnt",
      "conversion_cost",
      "conversion_rate",
      "cpm_platform"
    ],
    "appKey": 0,
    "queryDimensions": 1,
    "filters": {
      "campaignType": 0,
      "advType": 2
    },
    "extraRefer": {
      "pageId": "7363497363769507890",
      "moduleId": "7346249523100090378",
      "dataKey": "bp_promotion_chart_ad_bidding"
    },
    "isActive": True
  })
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://business.oceanengine.com',
    'priority': 'u=1, i',
    'referer': 'https://business.oceanengine.com/site/account-manage/ad/bidding/superior/account',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  }

  response = session.request("POST", url, headers=headers, data=payload)
  response_json = response.json()
  cost = response_json['data']['list'][0]['total']
