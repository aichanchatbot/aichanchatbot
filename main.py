import base64
import hashlib
import hmac
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

channel_secret = "806f6cc5d80d5899bc1a8c293f35603c"
body = ""
hash = hmac.new(channel_secret.encode('utf-8'),
    body.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hash)
# Compare X-Line-Signature request header and the signature

line_bot_api = LineBotApi('<channel access token>')

try:
    line_bot_api.reply_message('<reply_token>', TextSendMessage(text='Hello World!'))
except LineBotApiError as e:
    print("error")
    # error handle
