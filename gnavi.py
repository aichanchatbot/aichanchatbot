from janome.tokenizer import Tokenizer
from image_voice import image_voice
import csv
import requests
import json
from sound_rec import sound_rec
import sys
import os
import os.path
from data_path import gnavi_api_key
import time


#エラー時の処理
def error():
    f = open('temp.txt')
    int_data = f.read()
    f.close()
    temp = int(int_data)
    talk(temp)

#apiの終了
def api_close():
    print("AIchan>ばいば～い")
    end_text = "ばいばーい"
    image_voice(end_text)
    os.remove('temp.txt')
    os.remove('open_jtalk.wav')
    if os.path.exists('sample.wav'):
        os.remove('sample.wav')
    time.sleep(3)
    os.remove('text.txt')
    sys.exit()
    
# 形態素解析を行う
def token(text):
    t = Tokenizer()
    tokens = t.tokenize(u'{}'.format(text))
    for token in tokens:
        # 品詞を取り出し
        partOfSpeech = token.part_of_speech.split(',')[0]
        if partOfSpeech == u'名詞':
            return token.surface

# ぐるなびAPIへデータを送信
def gnaviserch(category, pref, area):
    #レストラン検索APIのURL
    url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"
    #パラメータの設定
    params={}
    params["keyid"] = "{}".format(gnavi_api_key()) #取得したアクセスキー
    params["category_s"] = "{}".format(category)
    params["pref"] = "{}".format(pref)
    params["freeword"] = "{}".format(area)

    #リクエスト結果
    result_api = requests.get(url, params)
    result_api = result_api.json()

    # エラーの場合
    if "error" in result_api:
        if "message" in result_api:
            print(u"{0}".format(result_api["message"]))
        else:
            text = "ごめんね。検索条件が間違ってるか、インターネットに繋がっていないよ。"
            print("AIchan:Gnaviserch>", text)
            image_voice(text)
            time.sleep(5)
            error()
    
    # ヒット件数取得
    total_hit_count = None
    if "total_hit_count" in result_api:
        total_hit_count = result_api["total_hit_count"]

    # ヒット件数が0以下、または、ヒット件数がなかったら最初に戻る
    if total_hit_count is None or total_hit_count <= 0:
        text = "ごめんね。お店がヒットしなかったよ。"
        print("AIchan:Gnaviserch>", text)
        image_voice(text)
        time.sleep(4)
        error()

    # レストランデータがなかったら最初に戻る
    if not "rest" in result_api:
        text = "ごめんね。お店が見つからなかったよ。"
        print("AIchan:Gnaviserch>", text)
        image_voice(text)
        time.sleep(4)
        error()

    # ヒット件数表示
    if total_hit_count > 10:
        print("AIchan:Gnaviserch>{0}件見つかったよ。件数が多いから10件だけ表示するね。".format(total_hit_count))
        print("_______________________")
        text = "{0}件見つかったよ。件数が多いから10件だけ表示するね。".format(total_hit_count)
        image_voice(text)
        time.sleep(5)
    else:
        print("AIchan:Gnaviserch>{0}件見つかったよ。".format(total_hit_count))
        print("_______________________")
        text = "{0}件見つかったよ。".format(total_hit_count)
        image_voice(text)
        time.sleep(4)
        
    hit = len(result_api['rest'])
    # ループで、ヒットした店名を表示させる
    for i in range(hit):
        print("店名:{}".format(result_api['rest'][i]["name"]))#店舗名称
        print("最寄り駅:{}".format(result_api['rest'][i]['access']["station"]))#駅名
        print(result_api['rest'][i]['access']["walk"] + "分")#徒歩（分）
        print("住所:{}".format(result_api['rest'][i]["address"]))#住所
        print("電話番号:{}".format(result_api['rest'][i]["tel"]))#電話番号
        print("営業時間:{}".format(result_api['rest'][i]["opentime"]))#営業時間
        print("休業日:{}".format(result_api['rest'][i]["holiday"]))#休業日
        print("URL:{}".format(result_api['rest'][i]["url"]))#PCサイトURL
        print("_______________________")

# 食べ物、お店のジャンルをcsvから抽出する
def category_serch(categorycode):
    csv_file = open("./dics/category_s.csv", "r", encoding="utf-8", errors="", newline="" )
    f = csv.DictReader(csv_file, delimiter=",", doublequote=False, lineterminator="\n", quotechar='"', skipinitialspace=True)
    try:
        for row in f:
            index = row.get("category_s_name").find(categorycode)
            if index != -1:
                return row["category_s_code"]
    except TypeError:
        text = "ごめんね。食べ物、お店の言い方を変えてみて。"
        print("AIchan:Gnaviserch>", text)
        image_voice(text)
        time.sleep(4)
        error()

# 都道府県をcsvから抽出する
def pref_serch(prefcode):
    csv_file = open("./dics/pref.csv", "r", encoding="utf-8", errors="", newline="" )
    f = csv.DictReader(csv_file, delimiter=",", doublequote=False, lineterminator="\n", quotechar='"', skipinitialspace=True)
    try:
        for row in f:
            index = row.get("pref_name").find(prefcode)
            if index != -1:
                return row["pref_code"]
    except TypeError:
        text = "ごめんね。都道府県名の言い方を変えてみて。"
        print("AIchan:Gnaviserch>", text)
        image_voice(text)
        time.sleep(4)
        error()

# 会話を実施する
def talk(set_mode):
    str_data = str(set_mode)
    f = open('temp.txt', mode='w', encoding='utf-8')
    f.write(str_data)
    f.close()
    text = "食べたい物かお店のジャンルを教えて！"
    print("AIchan:Gnaviserch>", text)
    image_voice(text)
    if set_mode == 1:
        text1 = input('あなた>>> ')
        if not text1:
            api_close()
            
    elif set_mode == 2:
        text1 = "{}".format(sound_rec())
        print("あなた>>>", text1)
        if not text1:
            api_close()
            
    else:
        api_close()
        
    text2 = token(text1)
    category_text = category_serch(text2)
    text = "どこの都道府県で探す？"
    print("AIchan:Gnaviserch>", text)
    image_voice(text)
    if set_mode == 1:
        text3 = input('あなた>>> ')
        if not text3:
            api_close()
            
    elif set_mode == 2:
        text3 = "{}".format(sound_rec())
        print("あなた>>>", text3)
        if not text3:
            api_close()
            
    else:
        api_close()

    text4 = token(text3)
    pref_text = pref_serch(text4)
    text = "駅名か地名を教えて"
    print("AIchan:Gnaviserch>", text)    
    image_voice(text)
    if set_mode == 1:
        text5 = input('あなた>>> ')
        if not text5:
            api_close()
            
    elif set_mode == 2:
        text5 = "{}".format(sound_rec())
        print("あなた>>>", text5)
        if not text5:
            api_close()
            
    else:
        api_close()

    area_text = token(text5)
    gnaviserch(category_text ,pref_text, area_text)
    os.remove('temp.txt')

if __name__ == "__main__":
    talk()
