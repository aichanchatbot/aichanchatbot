import json
import sys
import urllib.parse
import urllib.request

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
