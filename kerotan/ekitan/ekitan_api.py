# -*- coding: utf-8 -*-

import urllib
import requests
import json
import sys
import os
import traceback

from datetime import datetime
from django.conf import settings

# sys.path.append(settings.API_DIR) # runs on "python manage.py runserver" ok, "python ekitan_api.py" error
API_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'..', u'..', u'API')
sys.path.append(API_DIR)
from get_API_key import get_API_key


class Ekitan(object):

<<<<<<< HEAD
    # コンストラクタ（初期化）
    def __init__(self):
        # APIアクセスキー
        self.api_key = get_API_key("Ekitan API")

    # web検索
    def norikae_search(self, s_ido=35.696031, s_keido=139.690522, t_ido=35.681298, t_keido=139.766246):
        # 基本になるURL
        url = 'http://go.ekitan.com/asp-servlet/TrialAPI?'

        # 各種パラメータ
        # params = {
        #     "Query": "'{0}'".format(query),
        #     "Market": "'ja-JP'"
        # }
        V = "100"
        FC = "Norikae"
        LKEY = self.api_key           # !API key
        DT = "-1"                       # !date,半角数字8ケタ or -1当日
        # DW = -1                       # 曜日、0平日、1土曜、2日曜、-1当日
        # TM = "0000"                     # !time
        now = datetime.now()
        TM = now.strftime('%H') + now.strftime('%M')
        RP = "0"                        # !優先指定,0時刻、1料金、2乗換回数
        PN = "3"                        # !出力候補数、3,5,10,20
        SR = "0"                        # !発着指定, TMで指定した時間に出発するのか、到着するのかだと思う
        EP = "0"                        # !有料特急有無,0:なし,1:あり
        CHAR = "1"                      # !文字コード、0euc-jp, 1Shift_jis
        AN = "-1"                     # エリア番号。とりあえず-1でおｋ
        NF = "0"                        # 省略の有無、0正式名所、1略称
        # OF = "0"                        # 0XML or 1JSON
        OF = "1"                        # 0XML or 1JSON
        AIR = "0"                     # 航空会社優先指定、0なし、1JAL、2ANA、3SKY/ADO。緯度経度検索の場合、指定できない？
        SF = "10900"                    # 発駅コード、地点指定の場合は10900
        ST = "10901"                    # 着駅コード、地点指定の場合は10901
        LATF = str(s_ido)                    # !発地点緯度、SPEC パラメータで指定した書式で記述する。
        LNGF = str(s_keido)                  # !発地点経度
        LATT = str(t_ido)                    # !着地点緯度
        LNGT = str(t_keido)                  # !着地点経度
        # MVF=                        # 発地点から駅までの移動速度（m/min）,1~9000,たぶんデフォルト60
        # MVT=                        # 駅から着地点までの移動速度
        SRG = "100000"                        # 探索範囲,指定地点からの駅の探索範囲（m）, デフォルト5000
        # COORD=                      # 測地系指定。0 またはTKY:日本測地系、でふぉで０．１またはJGD(*6) :JGD2000(ITRF94)
        SPEC = "DEGREE"                 # 緯度経度書式。PART：度分秒（デフォ）、DEGREE：度小数点、SECOND：秒小数点、CSEC：1/100 秒
        # FSN=                        # 探索駅数。緯度経度地点の周辺駅とみなす駅数 1~10 の間で指定。デフォ10

        # フォーマットはjsonで受け取る
        # request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        request_url = url + "V=" + V + "&FC=" + FC + "&LKEY=" + LKEY \
                            + "&DT=" + DT + "&TM=" + TM + "&SR=" + SR + "&EP=" + EP \
                            + "&RP=" + RP + "&PN=" + PN + "&AN=" + AN + "&NF=" + NF \
                            + "&CHAR=" + CHAR \
                            + "&SPEC=" + SPEC \
                            + "&OF=" + OF \
                            + "&AIR=" + AIR \
                            + "&SF=" + SF + "&ST=" + ST \
                            + "&LATF=" + LATF + "&LNGF=" + LNGF \
                            + "&LATT=" + LATT + "&LNGT=" + LNGT \
                            + "&SRG=" + SRG
                            # + "&MVF=発地点から駅への移動速度" + "&MVT=駅から着地点への移動速度"\

        # print("request_url",request_url)

        results = self._search(request_url)
        # print(results)
        # 結果を返す
        return results

    # APIを叩く
    def _search(self, request_url):
        # 検索
        response = requests.get(request_url)
        # jsonを辞書型に変換
        response = response.json()
        # 経路検索結果のうち、最適な経路（のインデックス）を選択
        best_index = self.__response_best_selector(response)
        # 必要な情報だけ抽出
        response_filtered = self.__response_filter(response, best_index)

        # 結果を返す
        return (response, response_filtered)

    def __response_best_selector(self, response):
        # 経路検索結果のうち、最適な経路を選択し、そのindex番号を返す。
        # 最適とは、「移動時間*2000 + 料金」が最小のことを言う。
        indicater_of_best = []
        for (i, route) in enumerate(response["trainDoc"]["routeList"]["route"]):
            totalTime_min   = route["time"]["min"]["~T"] 	# 総移動時間（分）
            totalTime_hour  = route["time"]["hour"]["~T"] 	# 総移動時間（時間）
            fare            = route["fare"]["~T"] 			# 料金

            # 最適の指標「移動時間*2000 + 料金」を計算
            indicater_of_best.append((float(totalTime_min)*0.6 + float(totalTime_hour))*2000 + float(fare))

        # 最適指標が最小であった結果のインデックスを選択
        best_index = indicater_of_best.index(min(indicater_of_best))
        return best_index

    def __response_filter(self, response, best_index):
        # ------------------------------------------------------------------------------------------------------------------------------------------
        # 検索条件
        condition = {}

        pointFrom_latitude  = response["trainDoc"]["condition"]["pointFrom"]["coordinate"]["latitude"]["~T"] 	#出発地点緯度
        pointFrom_longitude = response["trainDoc"]["condition"]["pointFrom"]["coordinate"]["longitude"]["~T"] 	#出発地点経度
        pointFrom = {"pointFrom": {"latitude": pointFrom_latitude, "longitude": pointFrom_longitude}} 				#出発地点の緯度経度

        pointTo_latitude    = response["trainDoc"]["condition"]["pointTo"]["coordinate"]["latitude"]["~T"] 		#到着地点の緯度
        pointTo_longitude   = response["trainDoc"]["condition"]["pointTo"]["coordinate"]["longitude"]["~T"] 		#到着地点の経度
        pointTo = {"pointTo": {"latitude": pointTo_latitude, "longitude": pointTo_longitude}} 						#到着地点の緯度経度

        condition_time_hour = response["trainDoc"]["condition"]["time"]["hour"]["~T"] 	#出発時刻（時間）
        condition_time_min  = response["trainDoc"]["condition"]["time"]["min"]["~T"] 	#出発時刻（分）
        time = {"time": {"hour": condition_time_hour, "min": condition_time_min}} 			#出発時刻

        # 出発地点、到着地点、出発時刻を保存
        condition.update(pointFrom)
        condition.update(pointTo)
        condition.update(time)

        #------------------------------------------------------------------------------------------------------------------------------------------
        #経路情報
        line = []

        # 複数の経路検索結果のうち、最適な経路結果(best_index)の経路情報を保存する。
        for lineInfo in response["trainDoc"]["routeList"]["route"][best_index]["lineList"]["line"]:
            stationFrom_stationName = lineInfo["stationFrom"]["stationName"]["~T"] 				# 出発駅名
            stationFrom_latitude    = lineInfo["stationFrom"]["coordinate"]["latitude"]["~T"] 	# 出発駅の緯度
            stationFrom_longitude   = lineInfo["stationFrom"]["coordinate"]["longitude"]["~T"] 	# 出発駅の経度
            stationFrom_time_hour   = lineInfo["stationFrom"]["time"]["hour"]["~T"] 				# 出発時刻（時間）
            stationFrom_time_min    = lineInfo["stationFrom"]["time"]["min"]["~T"] 				# 出発時刻（分）
            stationFrom_time = {"hour": stationFrom_time_hour, "min": stationFrom_time_min} 		# 出発時刻
            # 出発の情報をまとめる
            stationFrom = {"stationFrom": {"stationName":stationFrom_stationName, "latitude": stationFrom_latitude, "longitude": stationFrom_longitude, "time": stationFrom_time}}

            stationTo_stationName   = lineInfo["stationTo"]["stationName"]["~T"] 				# 到着駅名
            stationTo_latitude      = lineInfo["stationTo"]["coordinate"]["latitude"]["~T"] 		#到着駅の緯度
            stationTo_longitude     = lineInfo["stationTo"]["coordinate"]["longitude"]["~T"] 	# 到着駅の経度
            stationTo_time_hour     = lineInfo["stationTo"]["time"]["hour"]["~T"] 				# 到着時刻（分）
            stationTo_time_min      = lineInfo["stationTo"]["time"]["min"]["~T"] 				# 到着時刻（分）
            stationTo_time = {"hour": stationTo_time_hour, "min": stationTo_time_min} 				# 到着時刻
            # 到着の情報をまとめる
            stationTo = {"stationTo": {"stationName": stationTo_stationName, "latitude": stationTo_latitude, "longitude": stationTo_longitude, "time": stationTo_time}}

            # 路線名
            lineName_tmp = lineInfo["lineName"]["~T"]
            lineName = {"lineName": lineName_tmp}

            # 1つの路線で移動できる、ある駅からある駅までの経路情報を1つの単位として、lineにアペンド
            # 例）A駅 -（JR）→ B駅 -(JR)→ C駅 -(地下鉄)→ D駅 なら、
            # A駅→C駅までの情報をlineの要素としてアペンド。A駅からC駅までの経由駅(B駅)の情報は無視。
            # C駅→D駅までの情報をlineの次の要素としてアペンド。
            lineInfo_temp = {}
            lineInfo_temp.update(stationFrom)
            lineInfo_temp.update(stationTo)
            lineInfo_temp.update(lineName)
            line.append(lineInfo_temp)

        fare            = response["trainDoc"]["routeList"]["route"][best_index]["fare"]["~T"] 			# 料金
        totalTime_hour  = response["trainDoc"]["routeList"]["route"][best_index]["time"]["hour"]["~T"] 	# 総移動時間（時間）
        totalTime_min   = response["trainDoc"]["routeList"]["route"][best_index]["time"]["min"]["~T"] 	# 総移動時間（分）
        totalTime       = {"hour": totalTime_hour, "min": totalTime_min} 									# 総移動時間

        # 上記の情報を経路情報としてまとめる
        route = {"lineList": line, "fare": fare, "totalTime": totalTime}
        # ------------------------------------------------------------------------------------------------------------------------------------------
        results = {"condition": condition, "route": route}

        return results


if __name__ == '__main__':
    # インスタンス作成
    ekitan = Ekitan()

    # 検索
    try:
        results, results_filtered = ekitan.norikae_search()
        # print(results)
        # print( json.dumps(results, indent=2) )
    except:
        print("--------------------------------------------")
        print("Error occured in ekitan search API.")
        print(traceback.print_exc())
        # print(traceback.print_tb(sys.exc_info()[2]))
        print("--------------------------------------------")
        raise

    # 結果をファイル出力（上書きするので注意）
    try:
        # with open("./ekitan_results/result_keiro.txt","w") as f:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/ekitan_results/result_keiro.txt", "w") as f:
            f.write(json.dumps(results, indent=2))
    except:
        print("--------------------------------------------")
        print("Error: Failed to output file of results of ekitan search .")
        print(traceback.print_exc())
        print("--------------------------------------------")
        # sys.exit()

    try:
        # with open("./ekitan_results/result_keiro_filtered.txt","w") as f:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/ekitan_results/result_keiro_filtered.txt", "w") as f:
            f.write(json.dumps(results_filtered, indent=2))
    except:
        print("--------------------------------------------")
        print("Error: Failed to output file of results of ekitan search .")
        print(traceback.print_exc())
        print("--------------------------------------------")
        # sys.exit()

    print("finished.")
