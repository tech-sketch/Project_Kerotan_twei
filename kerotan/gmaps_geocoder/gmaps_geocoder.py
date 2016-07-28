# -*- coding: utf-8 -*-
import googlemaps
import sys
import os
import traceback
import pprint

API_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'..', u'..', u'API')
sys.path.append(API_DIR)
from get_API_key import get_API_key


class GoogleMapsGeocoder(object):
    # コンストラクタ（初期化）
    def __init__(self):
        # APIアクセスキー
        self.api_key = get_API_key("Google Maps Geocoding API")

    def __result_filtering(self, geocode_result):
        # formatted_adress='Japan'なら、不正な住所入力などでアドレスが取れてない。
        # エラーを返す。
        # 検索結果は複数返すが、一番上の結果だけしか見ない。他は無視。簡易のため。
        if geocode_result[0]["formatted_address"] == 'Japan':
            raise Exception("Error:get_geocode. Formatted_address was 'Japan', inputed adress can't identify geocode. ")
        else:
            # 整形された住所と、latとlngが含まれたlocationを返す
            # 結果は複数返ってきてるが、一番目の結果だけreturn.
            return {"formatted_address": geocode_result[0]["formatted_address"], "location": geocode_result[0]["geometry"]["location"]}
        # latitude 	= geocode_result["geometry"]["location"]["lat"]
        # longitude 	= geocode_result["geometry"]["location"]["lng"]

    def get_geocode(self, adress="〒160-0023 東京都新宿区 西新宿８丁目１７−１"):
        try:
            # #API key load.
            # key=load_API_KEY("Google Maps Geocoding API")
            # auth
            gmaps = googlemaps.Client(key=self.api_key)

            # search condition
            componentRestrictions = {"country": 'JP'}

            # search
            geocode_result = gmaps.geocode(adress, componentRestrictions)

            # pprint.pprint( geocode_result )
            # pprint.pprint( geocode_result[0]["geometry"]["location"] )

            return self.__result_filtering(geocode_result)

        except Exception:
            raise
        except:
            raise

if __name__ == '__main__':
    GMgeocoder = GoogleMapsGeocoder()
    pprint.pprint(GMgeocoder.get_geocode("tis"))
