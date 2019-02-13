from unmo import Unmo
import subprocess
import knowledge
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

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
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)) #ここでオウム返しのメッセージを返します。
 
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def build_prompt(unmo):

    """AIインスタンスを取り、AIとResponderの名前を整形して返す"""

    return '{name}:{responder}> '.format(name=unmo.name,

                                         responder=unmo.responder_name)





if __name__ == '__main__':

    print('Unmo System prototype : AI')

    proto = Unmo('AI')

    while True:

        text = event.message.text

        if not text:

            break

        INDEX = text.find(u"調べ" or u"検索")

        if INDEX != -1:

            f = open('text.txt', mode='w', encoding='utf-8')
            f.write(text)
            f.close()

            send_api = knowledge.api_func()

            f = open('text.txt', 'r', encoding='shift-jis')
            contents = f.read()
            print("AI:Knowledge>",contents)


        else:

            try:
                response = proto.dialogue(text)

            except IndexError as error:
                print('{}: {}'.format(type(error).__name__, str(error)))
                print('警告: 辞書が空です。(Responder: {})'.format(proto.responder_name))

            else:
                print('{prompt}{response}'.format(prompt=build_prompt(proto),
                                                  response=response))


    proto.save()
