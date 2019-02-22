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
from main import reply_text, send_text
 
app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

port = int(os.getenv("PORT", 5000))
app.run(host="0.0.0.0", port=port)

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
#LINEのメッセージの取得と返信内容を設定
###############################################
 
#LINEでMessageEvent（メッセージを送信された）が発生した際、main.pyのreply_textへメッセージを渡す。
#main.pyのsend_textから送信内容を受け取る。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    r_text = event.message.text
    s_text = reply_text(r_text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}".format(s_text))
        
