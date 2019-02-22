import os
import re
from line_api import callback, handle_message
from docomo_api import docomo_api
from gnavi_api import gnaviserch
 

port()
callback()
handle_message()


def reply_text(text):
    
    INDEX = text.find(u"名前")
    INDEX2 = text.find(u"食べたい")
    INDEX3 = text.find(u"　")
    gnavi_message = text
    docomo_message = text
    
    if INDEX != -1:
        return "私の名前はaichanだよ"

    if INDEX2 != -1:
        return "県名　地域(駅名)　食べたい物(行きたいお店)を教えてくれたらお店を探すよ"

    if INDEX3 != -1:
        gnvi_response = gnaviserch(gnavi_message)
        return gnvi_response
        
    else:
        docomo_response = docomo_api(docomo_message)
        return docomo_response

