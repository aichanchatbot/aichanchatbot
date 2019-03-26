import os
import requests
import json
from datetime import datetime


def docomo_chat_api(text):
    # 環境変数取得docomoAPIキー
    APIKEY = os.environ["DOCOMO_API_KEY"]
    APPID = os.environ["DOCOMO_CHAT_APPID"]
    
    # リクエストボディ(JSON形式)
    send_data = {
        "language": "ja-JP",
        "botId": "Chatting",
        "appId": "{}".format(APPID),
        "voiceText": "",
        "clientData": {
            "option": {
                "nickname": "",
                "nicknameY": "",
                "sex": "",
                "age": "",
                "mode": "dialog"
                },
            },
        "appSendTime": "YYYY-MM-DD hh:mm:ss"
        }

    # リクエストヘッダ
    headers = {'Context-type': 'application/json'}

    # リクエストURL
    url = "https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY={}".format(APIKEY)
    send_data['voiceText'] = "{}".format(text)

    # 送信時間を取得
    send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_data['appSendTime'] = send_time

    # メッセージを送信
    r = requests.post(url, data=json.dumps(send_data), headers=headers)

    # レスポンスデータから返答内容を取得
    return_data = r.json()
    docomo_res = return_data['systemText']['expression']
    return docomo_res
