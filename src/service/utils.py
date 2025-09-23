"""
dumbass代码 别看 只用到了其中的上传文件的接口
"""
import json
import random
import string
import requests
from requests_toolbelt import MultipartEncoder


# ==================== 本地下载路径 ====================
REPTILE_FOLDER: str = 'D:/reptile'
DOWNLOAD_FOLDER: str = 'D:/reptile/download'
UPLOAD_FOLDER: str = 'D:/reptile/upload'
SAVE_FOLDER: str = 'D:/reptile/save'
SAVE_SRC_FOLDER: str = 'D:/reptile/save/src'
SAVE_RESULT_FOLDER: str = 'D:/reptile/save/result'
SAVE_RECORD_FOLDER: str = 'D:/reptile/save/record'
CHROME_PROFILE_FOLDER: str = 'D:/reptile/ChromeProfile'
DOWNLOAD_DAY_FOLDER: str = 'D:/reptile/downloadDay'
XML_FOLDER: str = 'D:/reptile/xml'
RE_XML_FOLDER: str = 'D:/reptile/re_xml'
UPLOADS_FOLDER: str = 'D:/reptile/uploads'

# ==================== 飞书相关 ====================
APP_ID: str = "cli_a441b931043b9013"
APP_SECRET: str = "5i78C0KAeSJuLDSzloEECdSCYRfrCST2"
TENANT_ACCESS_TOKEN_URL: str = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"  # 获得助手token地址
FEI_SHU_UPLOAD_IMAGE_URL: str = "https://open.feishu.cn/open-apis/im/v1/images"  # 图片上传接口
FEI_SHU_SEND_FILE_URL: str = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type="  # 发送文件/图片接口
FEI_SHU_SEND_FILE_GET_KEY_URL: str = "https://open.feishu.cn/open-apis/im/v1/files"  # 上传文件获取key

APP_ID_TWO: str = "cli_a6dc74a97afc500e"
APP_SECRET_TWO: str = "w51XBGKx2cv8gfR5FTOrPYhAZsOcvzut"

# def decode_app() -> tuple[str, str]:
#     """
#     返回RPA助手相关的app
#     :return:
#     """
#     app_id = APP_ID
#     app_secret = APP_SECRET
#
#     return app_id, app_secret


def __return_content(key: str, title: str):
    """
    发送图片，如果异常则艾特对应开发人员
    :param key: 文件/图片的飞书key
    :param title:  图片/文件的描述标题
    :return:
    """
    post_content = {
        "zh_cn": {
            "title": title,
            "content": []
        }
    }

    if "异常" in title:
        at = [{
            "tag": "at",
            "user_id": "64ebaa4c",
            "user_name": "林世武"
        }]
        post_content["zh_cn"]["content"].append(at)

    img = [
        {
            "tag": "img",
            "image_key": key
        }
    ]

    post_content["zh_cn"]["content"].append(img)

    return post_content


def get_tenant_access_token(app_id, app_secret) -> str:
    """
    返回RPA助手的token
    :return:
    """
    # app_id, app_secret = decode_app()
    rep = requests.request(
        method="post",
        url=TENANT_ACCESS_TOKEN_URL,
        data={
            "app_id": app_id,
            "app_secret": app_secret
        }
    )
    return rep.json()["tenant_access_token"]


def upload_image(app_id, app_secret, img_path):
    """
    上传图片,获取key
    """
    # 获取token
    tenant_access_token = get_tenant_access_token(app_id, app_secret)
    # 上传图片接口
    url = FEI_SHU_UPLOAD_IMAGE_URL
    # 图片信息
    form = {'image_type': 'message',
            'image': (open(img_path, 'rb'))}
    multi_form = MultipartEncoder(form)
    # 请求头
    headers = {'Content-Type': multi_form.content_type, 'Authorization': 'Bearer ' + tenant_access_token}
    response = requests.request("POST", url, headers=headers, data=multi_form)

    print("image_key:", response.json()['data']['image_key'])
    return response.json()['data']['image_key']


def __send_pic(app_id, app_secret, key: str, title: str, chat_id: str):
    """
    发送图片到飞书
    :param key: 获取上传图片飞书的key
    :param title: 文件描述
    :param chat_id: 群ID
    :return:
    """
    access_token = get_tenant_access_token(app_id, app_secret)
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    content = __return_content(key=key, title=title)

    data = {
        "receive_id": chat_id,
        "content": json.dumps(content),
        "msg_type": "post"
    }
    print(data)
    rep = requests.request(
        method="post",
        headers=headers,
        url=f"{FEI_SHU_SEND_FILE_URL}chat_id",
        data=json.dumps(data)
    )
    return rep.text


def send_pic(pic_path: str, title: str, chat_id: str, app_id: str = APP_ID, app_secret: str = APP_SECRET):
    key = upload_image(img_path=pic_path, app_id=app_id, app_secret=app_secret)
    rep_text = __send_pic(key=key, title=title, chat_id=chat_id, app_id=app_id, app_secret=app_secret)
    print(rep_text)


def send_file(access_token: str, file_path: str):
    # 随机生成16位的字符串
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    # 信息头字典，主要是为了加上boundary
    headers = {
        "Authorization": "Bearer " + access_token,
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary',
        'Accept': 'application/json, text/plain, */*, */*'
    }
    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # 参数以二进制的形式传输，只能上传excel
    file_names = file_path.split("/")
    print(file_names[-1])
    data = MultipartEncoder(
        fields={
            "file_type": "xlsx",
            "file_name": file_names[-1],
            'file': (
                file_names[-1], open(file_path, "rb"),
                content_type
            ),
            # 这段必加
            'boundary': '----WebKitFormBoundary' + random_string
        }
    )
    # 给Content-Type重新赋值
    headers['Content-Type'] = data.content_type
    rep = requests.post(
        FEI_SHU_SEND_FILE_GET_KEY_URL,
        data=data,
        headers=headers
    )
    return rep.json()["data"]["file_key"]


def send_feishu_file(file_path: str, chat_id: str, app_id: str = APP_ID, app_secret: str = APP_SECRET):
    access_token = get_tenant_access_token(app_id, app_secret)
    file_key = send_file(access_token=access_token, file_path=file_path)
    send_chat_url = f"{FEI_SHU_SEND_FILE_URL}chat_id"
    file_key_d = {
        "file_key": file_key
    }
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    data = {
        # "receive_id": "oc_bf9c0244225d9bdd99085c146986ce53",
        # "receive_id": "oc_fd65f3eef9f2ec531e61321067da77a3",
        "receive_id": chat_id,
        "msg_type": "file",
        "content": json.dumps(file_key_d),
        "uuid": ""
    }
    rep = requests.request(
        method="post", headers=headers, url=send_chat_url, data=json.dumps(data)
    )
    print(rep.text)
