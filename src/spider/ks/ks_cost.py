import datetime
import logging

import requests
import json

def get_ks_cost(session: requests.Session, refer_url: str) -> float:
  url = "https://agent.e.kuaishou.com/rest/dsp/agent/account/data/v2/queryDataReport"

  payload = json.dumps({
    "searchType": "ALL",
    "keyword": "",
    "userId": "",
    "dim": "ALL",
    "ucType": "ALL",
    "accountStatusEnum": "ALL",
    "attendTypes": [],
    "warnTypes": [],
    "advancedSearchConditions": [],
    "sortKey": "",
    "ascending": False,
    "pageInfo": {
      "currentPage": 1,
      "pageSize": 10,
      "totalCount": 0
    },
    "secondaryAgentKeyword": "",
    "platform": "DSP_PLATFORM",
    "dataFunctionEnum": "ACCOUNT_REPORT",
    "searchTypeValueMap": {
      "BATCH_ACCOUNT_NAME": "",
      "BATCH_USER_ID_EXACT": "",
      "BATCH_CORP_NAME": "",
      "BATCH_PRODUCT_NAME": ""
    },
    "ownerType": "ALL",
    "ownerKeyword": "",
    "startTime": int(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timestamp() * 1000),
    "endTime": int(datetime.datetime.combine(datetime.date.today(), datetime.time.max).timestamp() * 1000),
    "selectors": []
  })
  headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://agent.e.kuaishou.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': f'{refer_url}',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
  }

  response = session.request("POST", url, headers=headers, data=payload)
  response_json = response.json()
  cost = response_json['data']['summaryRow']['totalCharge'] / 1000
  logging.info(f"快手下的消耗为{cost}")
  return cost

def check(session: requests.Session):
  url = "https://agent.e.kuaishou.com/rest/dsp/agent/account/data/v2/queryDataReport"

  payload = json.dumps({
    "searchType": "ALL",
    "keyword": "",
    "userId": "",
    "dim": "ALL",
    "ucType": "ALL",
    "accountStatusEnum": "ALL",
    "attendTypes": [],
    "warnTypes": [],
    "advancedSearchConditions": [],
    "sortKey": "",
    "ascending": False,
    "pageInfo": {
      "currentPage": 1,
      "pageSize": 10,
      "totalCount": 0
    },
    "secondaryAgentKeyword": "",
    "platform": "DSP_PLATFORM",
    "dataFunctionEnum": "ACCOUNT_REPORT",
    "searchTypeValueMap": {
      "BATCH_ACCOUNT_NAME": "",
      "BATCH_USER_ID_EXACT": "",
      "BATCH_CORP_NAME": "",
      "BATCH_PRODUCT_NAME": ""
    },
    "ownerType": "ALL",
    "ownerKeyword": "",
    "startTime": int(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timestamp() * 1000),
    "endTime": int(datetime.datetime.combine(datetime.date.today(), datetime.time.max).timestamp() * 1000),
    "selectors": []
  })
  headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://agent.e.kuaishou.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://agent.e.kuaishou.com/data-analysis/account-analysis?__staffId__=2047262',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
  }

  response = session.request("POST", url, headers=headers, data=payload)
  response_json = response.json()
  res = response_json['data']['summaryRow']['totalCharge'] / 1000

