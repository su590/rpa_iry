import requests
import json

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
  "dataFunctionEnum": "ACCOUNT_REPORT",
  "searchTypeValueMap": {
    "BATCH_ACCOUNT_NAME": "",
    "BATCH_USER_ID_EXACT": "",
    "BATCH_CORP_NAME": "",
    "BATCH_PRODUCT_NAME": ""
  },
  "ownerType": "ALL",
  "ownerKeyword": "",
  "startTime": 1758470400000,
  "endTime": 1758556799999,
  "selectors": []
})
headers = {
  'accept': 'application/json',
  'accept-language': 'zh-CN,zh;q=0.9',
  'content-type': 'application/json',
  'origin': 'https://agent.e.kuaishou.com',
  'priority': 'u=1, i',
  'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'staff-id': '1001029303',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  'Cookie': 'apdid=4765d=1000015702185; userId=1538997212; userId=1538997212; bUserId=1000015702185; kwfv1=PnGU+9+Y8008S+nH0U+0mjPf8fP08f+98f+nLlwnrIP9+Sw/ZFGfzY+eGlGf+f+e4SGfbYP0QfGnLFwBLU80mYGAcU+e4fP/PUP/cU+A8fPnP7G9LlP0Ph8BLAGALUG9clP9pSPnLh+/cFweP7+nH7+/L98/bSwBLl+AHEPfcIPeGhP0qI+ePAP9GM8fzjPAH7P0q78/rh+0HA+ASf8eHl8W==; kuaishou.ad.login.identity=ChBhZC5sb2dpbi5rZXlOYW1lElB4mM5FX14t1bSPJlofV5aackuowr1q29MFqhWK-vF7VPjINCBUNMsIvQxCa9omCpGIFceEsjqU8DlwUZ_q6bDU0uuhOX3qWTJ6Qo8uHo0qShoSizv0OFb-h-v5nnkXLatSMR1fIiAZ_NRjVLJx_z3hSb7ggENY8LkhVpUvCRdFyhm8klwpzCgFMAE; Hm_lvt_e8002ef3d9e0d8274b5b74cc4a027d08=1758540167,1758540412; HMACCOUNT=6C56B7029C8B82B3; Hm_lvt_b97569d26a525941d8d163729d284198=1758540167,1758540412; Hm_lpvt_e8002ef3d9e0d8274b5b74cc4a027d08=1758541094; Hm_lpvt_b97569d26a525941d8d163729d284198=1758541094; kuaishou.ad.dsp.agent_st=ChhrdWFpc2hvdS5hZC5kc3AuYWdlbnQuc3QSsAHopLG_maIpAYs771S5ipJiYY5jowpzf95DXmBE_8KHxFx9_zAzGa2zkzbdLDdDwfJfJ85tyLu-Tvm21zzXYdtgA0f9xhvd1M2ntjrDy7UZPf9ycKRgrkcfvdCXHGqBQJAl1OhZvwyOEBO-7DtiLsFfUavh1nJBPWWgE1DFLYmYOeMtkwTSM7cDw2nYxPgJloNSsucptie53SZ3DavEcsQxE_DClW_8GvPwpciNhuyPdxoSj68V02bARguXsCufC7TxYbzJIiBWSdKiMaomiJ3i4_bkF8bLQFOsiDPfOPjsIl3_xtx--igFMAE; kuaishou.ad.dsp.agent_ph=e11171c48ac1ee4b7253fd589d635bfec058; JSESSIONID=0E2BAD4B3D29EFAEC3A90041E1AD1FB2; JSESSIONID=3727465BDC4B5043132EC3730BD15BE6'
}

response = requests.request("POST", url, headers=headers, data=payload)
response_json = response.json()
print(response.text)
