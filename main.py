from datetime import datetime
from flask import jsonify
from MadproBot import app

@app.route('/')
@app.route('/home')
def home():
    return jsonify({
        "message": "this endpoint is active"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    reply_to_line(request.json)
    return '', 200, {}

def reply_to_line(body):
    for event in body['events']:
        responses = []

        replyToken = event['replyToken']
        type = event['type']
        
        if type == 'message':
            message = event['message']
            
            if message['type'] == 'text':
                # そのままオウム返し
                responses.append(LineReplyMessage.make_text_response(message['text']))
            else:
                # テキスト以外のメッセージにはてへぺろしておく
                responses.append(LineReplyMessage.make_text_response('てへぺろ'))

        # 返信する
        LineReplyMessage.send_reply(replyToken, responses)


class LineReplyMessage:
    ReplyEndpoint = 'https://api.line.me/v2/bot/message/reply'
    AccessToken = '<LINE_CHANNEL_ACCESS_TOKEN>'

    @staticmethod
    def make_text_response(text):
        return {
            'type': 'text',
            'text': text
        }

    @staticmethod
    def send_reply(replyToken, messages):
        reply = {
            'replyToken': replyToken,
            'messages': messages
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(LineReplyMessage.AccessToken)
        }

        requests.post(
            LineReplyMessage.ReplyEndpoint,
            data=json.dumps(reply),
            headers=headers)
