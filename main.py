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

from wiki import wikipediaSearch

import pya3rt
 
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
#LINEのメッセージの取得と返信内容の設定
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #メッセージの判定
    INDEX1 = event.message.text.find('を教えて')

    #wiki検索
    if INDEX1 != -1:
        contents = event.message.text.replace('を教えて','')
        return_contents = wikipediaSearch(contents)
        
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=return_contents))

    #A3RTのTalkAPIにより応答
    else:
        reply_text = talkapi_response(event.message.text)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))
                
def talkapi_response(text):
    apikey = os.environ["YOUR_API_KEY"]
    client = pya3rt.TalkClient(apikey)
    response = client.talk(text)
    return ((response['results'])[0])['reply']

 
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
