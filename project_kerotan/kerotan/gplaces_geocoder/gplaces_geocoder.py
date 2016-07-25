# -*- coding: utf-8 -*-
import googlemaps
import sys
import os
import traceback
import pprint

from googleplaces import GooglePlaces, types, lang

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../API/')
from APIkey_load_yaml import load_API_KEY


class GooglePlacesGeocoder(object):
    # コンストラクタ（初期化）
    def __init__(self):
        # APIアクセスキー
        self.api_key = load_API_KEY("Google Places API")

    def get_address(self, place):
        try:
            google_places = GooglePlaces(self.api_key)
            query_result = google_places.text_search(query="japan " + place, language="ja", radius=100000, location="Japan")
            # google places apiを利用したgeocodeの取得
            # 正式名称での実行を推奨 / 正式名称であれば第一候補に目的地が現れる可能性が非常に高い
            # pprint.pprint(GMgeocoder.get_address("TIS株式会社 名古屋本社"))
            # return query_result.places[0].geo_location
            query_result.places[0].get_details()
            location = {"name":query_result.places[0].name, "formated_address":query_result.places[0].formatted_address, "location":{"lat":float(query_result.places[0].geo_location["lat"]), "lng":float(query_result.places[0].geo_location["lng"])}}
            return location

        except Exception:
            raise
        except:
            raise


if __name__ == '__main__':
    GPgeocoder = GooglePlacesGeocoder()
    pprint.pprint(GPgeocoder.get_address("幕張メッセ"))