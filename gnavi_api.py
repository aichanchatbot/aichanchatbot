import csv
import requests
import json


def gnaviserch(word):
    #レストラン検索APIのURL
    url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"
    #パラメータの設定
    params={}
    params["keyid"] = "af8de7fc02ff348220ba62e3c05de7f6" #取得したアクセスキー
    params["freeword"] = "{}".format(word)

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

        
    hit = len(result_api['rest'])
    # ループで、ヒットした店名を表示させる
    for i in range(hit):
        return "店名:{}".format(result_api['rest'][i]["name"])"URL:{}".format(result_api['rest'][i]["url"])#PCサイトURL
