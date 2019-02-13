import requests
import json
from datetime import datetime

def api_func():

    """入力内容をtemp.txtから取得"""
    f = open('text.txt', 'r', encoding='utf-8')
    contents = f.read()

    """APIキー"""
    APIKEY = "6b596f636d5262304453596f6a4d646a653643514f33446b586a57754831764462376a50427453794d5130"

    """リクエストボディ(JSON形式)"""
    send_data = {
        "language": "ja-JP",
        "botId": "Knowledge",
        "appId": "c36384ee-626e-4aab-8d4f-d32fd5b1634b",
        "voiceText": "",
        "appRecvTime": "YYYY-MM-DD hh:mm:ss",
        "appSendTime": "YYYY-MM-DD hh:mm:ss"
        }

    """リクエストヘッダ"""
    headers = {'Context-type': 'application/json'}

    """リクエストURL"""
    url = "https://api.apigw.smt.docomo.ne.jp/naturalKnowledge/v1/dialogue?APIKEY={}".format(APIKEY)

    """[voiceText]内に入力内容を書き込み"""
    send_data['voiceText'] = contents
    
    """送信時間を取得"""
    send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_data['appSendTime'] = send_time

    """メッセージを送信"""
    r = requests.post(url, data=json.dumps(send_data), headers=headers)
    
    """レスポンスデータから返答内容を取得"""
    return_data = r.json()
    return_message = return_data["systemText"]["expression"]

    """返答内容を音声出力用text.txtに書き込み(改行と*を削除)"""
    text = return_message.replace('\n','')
    text2 = text.replace('\r','')
    text3 = text2.replace('*','')
    f = open('text.txt', mode='w', encoding='shift-jis')
    f.write(text3)
    f.close()
    
