import requests
 
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

def post_text(reply_token, text):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer" "<tkRCRSMlOvPMRWBmcARN3isuPn0uOwUfi8BYH2369KNNNAPMJuu2i0KmTHr7HnC609rktbNOBXk9ZeUz1c9KNTrLNPVFSJg8C+4Os4d5n+oklTOXPrqkDuG+dsMzWKIRplvCuid+eAwpXNOZMDSXbgdB04t89/1O/w1cDnyilFU=>"
    }
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type": "text",
                    "text": "こんにちは"
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))
