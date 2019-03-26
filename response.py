import re
import shelve
from docomo_api import docomo_chat_api, docomo_shiritori_api


def response(text):
    # しりとりモードの処理
    INDEX1 = text.find("しりとり")
    m = shelve.open("/tmp/mode")
    INDEX2 = m['string'].find("srtr")
    m.close()
    INDEX3 = text.find("はい")

    # しりとりモードの処理
    if INDEX1 != -1:
        m = shelve.open("/tmp/mode")
        m["string"] = "srtr"
        m.close()
        texts = docomo_shiritori_api(text)
        return re_text(texts)
    elif INDEX2 != -1:
        if INDEX3 != -1:
            texts = docomo_shiritori_api(text)
            m = shelve.open("/tmp/mode")
            m["string"] = ""
            m.close()
            return re_text(texts)
        else:
            texts = docomo_shiritori_api(text)
            return re_text(texts)
    
    # チャットモードの処理    
    else:
        m = shelve.open("/tmp/mode")
        m["string"] = "dialog"
        m.close()
        texts = docomo_chat_api(text)
        return re_text(texts)
        

def re_text(text):
    text1 = re.sub("僕|ぼく|ボク|俺", "私", text)
    text2 = text1.replace("名前はゼロ", "名前はAI")
    return text2

    
