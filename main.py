from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import requests
import json
from datetime import datetime
 
app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

## 1 ##
###############################################
#Webhookからのリクエストをチェック
###############################################

# リクエストヘッダーから署名検証のための値を取得します。
# リクエストボディを取得します。
# 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
# 署名検証で失敗した場合、例外を出す。
# handleの処理を終えればOK

@app.route("/callback", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']
 
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


   
   
   
## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################



## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
 line_bot_api.reply_message(
  event.reply_token,
  TextSendMessage(text=docomo_res)) 
 docomo_res = response
 
def docomo_api(event.message.text):
 # APIキー
 APIKEY = "6b596f636d5262304453596f6a4d646a653643514f33446b586a57754831764462376a50427453794d5130"
 
 # リクエストボディ(JSON形式)
 send_data = {
  "language": "ja-JP",
  "botId": "Chatting",
  "appId": "67552b25-9624-4fd8-8d59-6c4fc093ef9e",
  "voiceText": "",
  "appSendTime": "YYYY-MM-DD hh:mm:ss"
  }
 
 # リクエストヘッダ
 headers = {'Context-type': 'application/json'}
 # リクエストURL
 url = "https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY={}".format(APIKEY)
 send_data['voiceText'] = event.message.text
 # 送信時間を取得
 send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 send_data['appSendTime'] = send_time
 # メッセージを送信
 r = requests.post(url, data=json.dumps(send_data), headers=headers)
 # レスポンスデータから返答内容を取得
 return_data = r.json()
 response = return_data['systemText']['expression']

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
