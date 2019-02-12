from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('tkRCRSMlOvPMRWBmcARN3isuPn0uOwUfi8BYH2369KNNNAPMJuu2i0KmTHr7HnC609rktbNOBXk9ZeUz1c9KNTrLNPVFSJg8C+4Os4d5n+oklTOXPrqkDuG+dsMzWKIRplvCuid+eAwpXNOZMDSXbgdB04t89/1O/w1cDnyilFU=')

try:
    line_bot_api.reply_message('<reply_token>', TextSendMessage(text='Hello World!'))
