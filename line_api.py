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
from docomo_api import docomo_api
from gnavi_api import talk1, talk2, talk3, talk4
 
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
#LINEのメッセージの取得と返信パターンを判定し、返信内容を設定
###############################################
 
#LINEでMessageEvent（メッセージを送信された）が発生した際、メッセージ内容を判定し、
#docomo_apiまたはgnavi_apiに処理を渡し、返信内容を受け取る。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    INDEX = event.message.text.find(u"名前")
    INDEX2 = event.message.text.find(u"食べたい")
    gnavi_message = event.message.text
    docomo_message = event.message.text
    f = open('temp.txt', mode='r', encoding='utf-8')
    
    if INDEX != -1:
        f.close()
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="私の名前はaichanだよ"))

    if INDEX2 != -1:
        f.close()
        gnavi_message1 = talk1()
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}".format(gnavi_message1)))

    if f in '2':
        f.close()
        gnavi_message2 = talk2(gnavi_message)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}".format(gnavi_message2)))

    if f in '3':
        f.close()
        gnavi_message3 = talk3(gnavi_message)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}".format(gnavi_message3)))

    if f in '4':
        f.close()
        gnavi_message4 = talk4(gnavi_message)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}".format(gnavi_message4)))

    else:
        f.close()
        docomo_response = docomo_api(docomo_message)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}".format(docomo_response)))

        
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
