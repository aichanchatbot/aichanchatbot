import json
import sys
import urllib.parse
import urllib.request
import random

WEATHER_URL="http://weather.livedoor.com/forecast/webservice/json/v1?city=%s"
CITY_CODE="230010" # AICHI(NAGOYA)
#TODAY=0
#TOMMOROW=1

def get_weather_info():
    try:
        url = WEATHER_URL % CITY_CODE
        html = urllib.request.urlopen(url)
        html_json = json.loads(html.read().decode('utf-8'))
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)
    return html_json

def set_weather_info(weather_json, day):
    min_temperature = None
    max_temperature = None
    try:
        date = weather_json['forecasts'][day]['dateLabel'] #dateに変更すると日付表示可能
        city = weather_json['location']['city']
        weather = weather_json['forecasts'][day]['telop']
        #max_temperature = weather_json['forecasts'][day]['temperature']['max']['celsius']
        #min_temperature = weather_json['forecasts'][day]['temperature']['min']['celsius']
    except TypeError:
        # temperature data is None etc...
        pass
    msg = "%sの%sの天気は%sだよ。" % \
               (date, city, weather)
    #msg = "%s\n天気: %s\n最低気温 : %s度\n最高気温: %s度" % \
               #(date, weather, min_temperature, max_temperature)
    return msg

def weather(info_day):
    weather_json = get_weather_info()
    for day in [info_day]:
        msg = set_weather_info(weather_json, day)
        return msg

def set_weather_date(text):
    index1 = text.find('今日')
    index2 = text.find('明日')
    index3 = text.find('明後日')

    if index1 != -1:
        msg = weather(0)
        texts = set_msg(msg)
        return texts

    elif index2 != -1:
        msg = weather(1)
        texts = set_msg(msg)
        return texts

    elif index3 != -1:
        msg = weather(2)
        texts = set_msg(msg)
        return texts

    else:
        msg = weather(0)
        texts = set_msg(msg)
        return texts

def set_msg(text):
    text1 = "{}".format(text)
    text2 = random.choice(('お散歩できないなぁ。。。', '外で遊びたいのに。。。'))
    text3 = random.choice(('雨は降らないみたい。', 'お散歩行けるね。'))
    text4 = random.choice(('お散歩日よりだね。', 'お出かけしよう。'))

    index10 = text1.find('雨')
    index11 = text1.find('曇')
    index12 = text1.find('晴')
                           
    if index10 != -1:
        texts = str(text1)+str(text2)
        return texts
    elif index11 != -1:
        texts = str(text1)+str(text3)
        return texts
    elif index12 != -1:
        texts = str(text1)+str(text4)
        return texts
    else:
        return text

    
