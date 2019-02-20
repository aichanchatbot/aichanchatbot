import os
import requests
import json
from datetime import datetime


def docomo_api(text):
    # APIキー
    APIKEY = "6b596f636d5262304453596f6a4d646a653643514f33446b586a57754831764462376a50427453794d5130"
    # リクエストボディ(JSON形式)
    send_data = {
        "language": "ja-JP",
        "botId": "Chatting",
        "appId": "67552b25-9624-4fd8-8d59-6c4fc093ef9e",
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
