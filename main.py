import requests
 
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

def post_text(reply_token, text):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {tMCU/hu7j4Pq0ePqkb2cqytGQkjgK0Gh3y6a4viauHuYzE+ZTHvQDJRZc4NcFjhlw/VHwvNiYGPdkLMoRqFbv/IrXVAQAUZcq4o9Ki98eu7mfNYEUsRMIfK7Vwy2TWDk9z5lFqkihrMH4cOGlIKImgdB04t89/1O/w1cDnyilFU=}"
    }
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": text
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))
