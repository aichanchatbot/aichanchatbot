import re
import shelve
from docomo_api import docomo_chat_api


def response(text):
    texts = docomo_chat_api(text)
    return re_text(texts)
        

def re_text(text):
    text1 = re.sub("僕|ぼく|ボク|俺", "私", text)
    text2 = text1.replace("名前はゼロ", "名前はAI")
    return text2

    
