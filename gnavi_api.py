from janome.tokenizer import Tokenizer
import csv
import requests
import json

def token(text):
    t = Tokenizer()
    tokens = t.tokenize(u'{}'.format(text))
    for token in tokens:
        # 品詞を取り出し
        partOfSpeech = token.part_of_speech.split(',')[0]
        if partOfSpeech == u'名詞':
            return token.surface


def gnaviserch(area):
    #レストラン検索APIのURL
    url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"
    #パラメータの設定
    params={}
    params["keyid"] = "041bf926060de0bdcbe537265b4c78ea" #取得したアクセスキー
    params["category_s"] = "{}".format(category)
    params["pref"] = "{}".format(pref)
    params["freeword"] = "{}".format(area)

    #リクエスト結果
    result_api = requests.get(url, params)
    result_api = result_api.json()

    # エラーの場合
    if "error" in result_api:
        if "message" in result_api:
            return (u"{0}".format(result_api["message"]))
        else:
            return "ごめんね。お店のデータが見つからなかったよ"
    
    # ヒット件数取得
    total_hit_count = None
    if "total_hit_count" in result_api:
        total_hit_count = result_api["total_hit_count"]

    # ヒット件数が0以下、または、ヒット件数がなかったら最初に戻る
    if total_hit_count is None or total_hit_count <= 0:
        return "指定した内容ではヒットしなかったよ"

    # レストランデータがなかったら最初に戻る
    if not "rest" in result_api:
        return "レストランデータが見つからなかったよ"

    # ヒット件数表示
    if total_hit_count > 10:
        return "AI:Gnaviserch>{0}件見つかったよ。件数が多いから10件だけ表示するね。".format(total_hit_count)
        return "_______________________"
    else:
        return "AI:Gnaviserch>{0}件見つかったよ。".format(total_hit_count)
        return "_______________________"
        
    hit = len(result_api['rest'])
    # ループで、ヒットした店名を表示させる
    for i in range(hit):
        return "店名:{}".format(result_api['rest'][i]["name"])#店舗名称
        return "最寄り駅:{}".format(result_api['rest'][i]['access']["station"])#駅名
        return result_api['rest'][i]['access']["walk"] + "分"#徒歩（分）
        return "住所:{}".format(result_api['rest'][i]["address"])#住所
        return "電話番号:{}".format(result_api['rest'][i]["tel"])#電話番号
        return "営業時間:{}".format(result_api['rest'][i]["opentime"])#営業時間
        return "休業日:{}".format(result_api['rest'][i]["holiday"])#休業日
        return "URL:{}".format(result_api['rest'][i]["url"])#PCサイトURL
        return "_______________________"


def category_serch(categorycode):
    csv_file = open("/app/data/category_s.csv", "r", encoding="utf-8", errors="", newline="" )
    f = csv.DictReader(csv_file, delimiter=",", doublequote=False, lineterminator="\n", quotechar='"', skipinitialspace=True)
    try:
        for row in f:
            index = row.get("category_s_name").find(categorycode)
            if index != -1:
                print(row["category_s_code"])
                return row["category_s_code"]
    
    except TypeError:
        f = open('/app/temp.txt', mode='w', encoding='utf-8')
        f.write('')
        f.close()
        return "ごめんね。言葉として認識できなかったよ。"

def pref_serch(prefcode):
    csv_file = open("/app/data/pref.csv", "r", encoding="utf-8", errors="", newline="" )
    f = csv.DictReader(csv_file, delimiter=",", doublequote=False, lineterminator="\n", quotechar='"', skipinitialspace=True)
    try:
        for row in f:
            index = row.get("pref_name").find(prefcode)
            if index != -1:
                print(row["pref_code"])
                return row["pref_code"]
    except TypeError:
        f = open('/app/temp.txt', mode='w', encoding='utf-8')
        f.write('')
        f.close()
        return "ごめんね。言葉として認識できなかったよ。"

def talk1():
    f = open('/app/temp.txt', mode='w', encoding='utf-8')
    f.write('2')
    f.close()
    return "食べたい物、または何のお店のジャンルを教えて！"

def talk2(text):
    token_text = token(text)
    category_text = category_serch(token_text)
    f = open('/app/category.txt', mode='w', encoding='utf-8')
    f.write(category_text)
    f.close()
    f = open('/app/temp.txt', mode='w', encoding='utf-8')
    f.write('3')
    f.close()
    return "どこの都道府県で探す？"

def talk3(text):
    token_text = token(text)
    pref_text = pref_serch(token_text)
    f = open('/app/pref.txt', mode='w', encoding='utf-8')
    f.write(pref_text)
    f.close()
    f = open('/app/temp.txt', mode='w', encoding='utf-8')
    f.write('4')
    f.close()
    return "駅名か地名を教えて"

def talk4(text):
    token_text = token(text)
    gnaviserch(token_text)
    f = open('/app/temp.txt', mode='w', encoding='utf-8')
    f.write('')
    f.close()
    return gnaviserch

if __name__ == "__main__":
    talk1()
