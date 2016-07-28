# -*- coding: utf-8 -*-
import os
import sys
import traceback
import json
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from kerotan.forms import AddressForm

from .ekitan.ekitan_api import Ekitan
from .gmaps_geocoder.gmaps_geocoder import GoogleMapsGeocoder
from .bing_news.bing_api import Bing

API_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'..', u'..', u'API')
sys.path.append(API_DIR)
from get_API_key import get_API_key


def display_google_map(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        company_address = {
            "TIS": "東京都新宿区 西新宿８丁目１７−１",
            "幕張メッセ": "〒261-0023 千葉市美浜区中瀬2-1",
            "新宿駅": "〒160-0023 東京都新宿区西新宿１丁目１−３",
            "東京駅": "〒100-0005 東京都千代田区丸の内1 丁目 呑んき１丸の内北口店 9",
            "大阪駅": "大阪府大阪市北区梅田３丁目１−１",
            "立命館大学": "〒525-8577 滋賀県草津市野路東１丁目1-1",
        }
        company_overview = {
            "TIS": "TIS株式会社（ティーアイエス）は国内大手システムインテグレーター。傘下にインテック、アグレックス、クオリカ、AJSなどを擁するTISインテックグループの中核企業である。",
            "幕張メッセ": "幕張メッセ（まくはりメッセ、Makuhari Messe）は、千葉県千葉市美浜区にある大型の会議・展示施設である。また、株式会社幕張メッセは、これを運営する企業である。",
            "新宿駅": "新宿駅（しんじゅくえき）は、東京都新宿区・渋谷区にある、東日本旅客鉄道（JR東日本）・京王電鉄・小田急電鉄・東京地下鉄（東京メトロ）・東京都交通局（都営地下鉄）の駅である。",
            "東京駅": "東京駅（とうきょうえき）は、東京都千代田区丸の内一丁目にある、東日本旅客鉄道（JR東日本）・東海旅客鉄道（JR東海）・東京地下鉄（東京メトロ）の駅である。",
            "大阪駅": "大阪駅（おおさかえき）は、大阪府大阪市北区梅田三丁目にある、西日本旅客鉄道（JR西日本）の駅である。",
            "立命館大学": "立命館大学（りつめいかんだいがく、英語: Ritsumeikan University）は、京都府京都市中京区西ノ京朱雀町1に本部を置く日本の私立大学である。1922年に設置された。大学の略称は立命、立命館、立命大。近畿圏では立大も使用される[1]。"
        }
# 		company_overview={
# 			"TIS":"TIS株式会社（初代）は、1971年（昭和46年）4月、三和銀行および三和グループを中心に大阪市東区（現在の大阪市中央区）に\
# 株式会社東洋情報システム（資本金6億円）として設立された。現在の法人は、2016年（平成28年）7月にITホールディングス株式会社がTIS株式会社（初代）を\
# 吸収合併し、商号変更したものである。三和グループに属する企業で構成されるみどり会の会員企業でもある。\
# JCBを中心としたクレジットカード会社の基幹システムなどに強みを持ち、国内シェアは5割弱で首位。",
# 			"幕張メッセ":"幕張メッセのメッセとは、ドイツ語の'見本市'の意味を指す'Messe'に由来する。1989年（平成元年）10月9日に開業した。\
# 現在は、東京国際展示場（東京ビッグサイト、東西合計）に次ぐ国内2番目の規模となっている。運営会社は、1986年（昭和61年）4月30日に設立され、\
# 2005年（平成17年）7月1日に社名を株式会社日本コンベンションセンター（Nippon Convention Center）から株式会社幕張メッセに変更した。\
# 当館の整備費は増設分を合わせると約558億円を投じており、年間の維持管理費が約20億円掛かるとされており、千葉県と千葉市の公費による一部負担が続いている。\
# しかし、都心から近い東京国際展示場開業の影響を受け、2011年（平成23年）に東京モーターショーが東京ビッグサイトへ移るなど利用は伸び悩み、\
# 2013年（平成23年）度の稼働率は約40%となり、横浜市のパシフィコ横浜の稼働率の約70%を大きく下回っている。",
# 			"新宿駅":"東京の副都心・新宿に位置するターミナル駅である。1885年（明治18年）に日本鉄道により現在の山手線が開業したのが当駅の始まりである。\
# 4年後の1889年（明治22年）には南豊島郡淀橋町となる。開業時から新宿を副都心にする計画が発表されるまでは当駅周辺はまだ街の外れであり利用客は少ないものだったが、\
# 大正期に入り次第に市街地が拡大するにつれ、多くの私鉄が乗り入れるようになる。ターミナルとなって周辺が発展するにつれて利用客は増え続け、1931年には私鉄や国鉄などを合わせた\
# 利用者数で日本一になった[1]。そして、1966年（昭和41年）の乗車人数では、国鉄池袋駅の41万67人を抜いて、当駅が41万69人と日本一になっている。\
# さらに1960年代から当駅西側一帯で進められた新宿副都心計画によって、70年代には多くの超高層ビルが建てられ利用者の増加に拍車がかかった。\
# 現在ではJR・私鉄・地下鉄の多くの路線が周辺地域のベッドタウンとを結んでおり、多くのビジネス客が利用する。さらに、当駅周辺は日本最大の繁華街・歓楽街となっており、\
# 昼夜を問わず人の流れが絶えない。JRの駅を中心に東・西・南口、周辺の各地下鉄駅、商業施設などが通路や地下街などで広範囲に連絡している。\
# 一日平均乗降者数は約335万人（2013年）[3]と世界一（ギネス世界記録認定）多い駅であり、地下道などで接続する西武新宿駅まで含めると約358万人（2013年）となり、\
# この数字は横浜市の人口に匹敵する。年間の乗降客数に直すと約13億人となりインドの人口をも上回る規模となる。",
# 			"東京駅":"東京の表玄関とも言うべきターミナル駅で、特に東海道新幹線と東北新幹線の起点となっており、全国の新幹線網における最大の拠点となっている。\
# また、東海道本線や東北本線など主要幹線の起点駅でもある。当駅から乗り換えなしで実に33都道府県[1]と結んでおり、1日当たりの列車発着本数は約3000本という日本を代表する\
# ターミナル駅の一つである。プラットホームの数は日本一多く、在来線が地上5面10線と地下4面8線の合計9面18線、新幹線が地上5面10線、地下鉄は地下1面2線を有しており、\
# 面積は東京ドーム約3.6個分に相当する。赤レンガ造りの丸の内口駅舎は辰野金吾らが設計したもので、1914年に竣工、2003年に国の重要文化財に指定されている。\
# 「関東の駅百選」認定駅でもある。",
# 			"大阪駅":"大阪府の代表駅（府庁所在地駅）として第1回近畿の駅百選にも選定されている西日本最大の駅。駅長が配置された直営駅であり、\
# 管理駅として東海道本線の塚本駅を管轄している。JRの特定都区市内制度における「大阪市内」に属する駅であり、運賃計算の中心駅となる。また、アーバンネットワークの運行の要衝となる駅で、\
# 運行系統の軸をなしている。大阪市街の北玄関である梅田に位置し、駅前や駅の東側・南側を中心に繁華街が広がっている。\
# 東京・山陽・九州方面への長距離列車については、1964年開業の新大阪駅を発着する東海道・山陽新幹線に地位を譲ったものの、当駅は現在でも北陸方面との特急の始発・終着駅であり、\
# 新快速を始めとする京阪神の都市間連絡列車や、北近畿・山陰方面との特急、東京駅発着の寝台特急などの在来線特急も発着している。\
# かつては東北・北海道方面に向かう夜行列車も発着していたが、2015年3月のダイヤ改正で寝台特急トワイライトエクスプレスが廃止されたことで東北・北海道方面を行き来する夜行列車は全て消滅した。\
# これによって大阪駅を起点、終点とする夜行列車は全て消滅した。ただし、トワイライトエクスプレスは同年5月16日(土)に山陽方面のツアー列車として復活した。\
# 貨物列車は北方貨物線および梅田貨物線（いずれも通称）を利用するため大阪駅を通過しない。"}

        if form.is_valid():
            print("form.is_valid() ok")
            # 出発フォームの入力内容が、辞書に登録されているかどうか確認。
            try:
                # 登録されていれば、辞書から住所を取得し、出発住所とする
                start_company = company_address[form.cleaned_data["start_address"]]
            except:
                # 入力内容が、辞書に登録されていなければ、入力内容を出発住所とする。
                start_company = form.cleaned_data["start_address"]

            # 到着フォームでも同様の処理。
            try:
                arriv_company = company_address[form.cleaned_data["arriv_address"]]
                # 到着の方が辞書に含まれるなら、概要とニュースと取得する。ので、フラグを立てる。
                FLAG_getOverviewNews = 1
            except:
                # 入力内容が、辞書に登録されていなかった。
                arriv_company = form.cleaned_data["arriv_address"]
                FLAG_getOverviewNews = 0

            # ---------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------
            # geocode,会社概要、ニュースを取得する。
            try:
                # Get geocode by Google Maps API.
                try:
                    print("try get_geocode : ", end="")
                    gmg = GoogleMapsGeocoder()
                    geocode = {}
                    geocode.update({"start": gmg.get_geocode(start_company)["location"]})
                    geocode.update({"arriv": gmg.get_geocode(arriv_company)["location"]})
                    print("finished.")
                except Exception as e:
                    # 入力された住所から、geocodeを特定できない。
                    # 再入力させるために、入力画面に戻す。
                    print("--------------------------------------------")
                    print(type(e))
                    print(e)
                    print(traceback.print_exc())
                    print("--------------------------------------------")
                    raise
                except:
                    # 謎のエラー発生時
                    print("--------------------------------------------")
                    print("謎Error in GoogleMaps.")
                    print(traceback.print_exc())
                    print("--------------------------------------------")
                    raise

                # ---------------------------------------------------------------------------------
                # 会社概要を取得
                if FLAG_getOverviewNews == 1:
                    try:
                        # 辞書からとってくるだけ。
                        print("try company_overview : ", end="")
                        overview = company_overview[form.cleaned_data["arriv_address"]]
                        image_company_chart = "/static/img/TIS_chart.png"
                        image_company_building = "/static/img/TIS_building.png"
                        print("finished.")
                    except:
                        # 謎のエラー発生時.
                        print("--------------------------------------------")
                        print("謎Error in 会社概要.")
                        print(traceback.print_exc())
                        print("--------------------------------------------")
                        raise
                elif FLAG_getOverviewNews == 0:
                    # 概要はとってこない
                    print("getting overview was passed.")
                    overview = ""
                    image_company_chart = ""
                    image_company_building = ""
                else:
                    # ありえない
                    raise

                # ---------------------------------------------------------------------------------
                # ニュースを取得
                try:
                    # bing search APIで、関連ニュースをとってくる
                    print("try bing.web_search : ", end="")
                    bing = Bing()
                    keys = ["Title", "Url", "Source", "Description", "Date"]
                    query = form.cleaned_data["arriv_address"]
                    news = bing.web_search(query, 5, keys)
                    print("finished.")
                    print("news", json.dumps(news, indent=2))
                except (TypeError, ConnectionAbortedError, ConnectionResetError, MaxRetryError, requests.packages.urllib3.exceptions.MaxRetryError, AttributeError, TransportError, googlemaps.exceptions.TransportError, ConnectionError, requests.exceptions.ConnectionError, NewConnectionError):
                    # 一分間に連続してリクエスト送ると、回数制限に引っかかってエラー。たぶん。その場合、空のニュースを返すことにする。
                    # raiseはしない。
                    print("--------------------------------------------")
                    print("BingSearchAPI回数制限に引っかかりました。時間を置きましょう。")
                    print(traceback.print_exc())
                    print("--------------------------------------------")
                    news = []
                except FileNotFoundError:
                    # 検索結果のファイル出力時のエラー。
                    # raiseはしない。
                    print("--------------------------------------------")
                    print("BingSearchAPIの結果出力時のエラー。")
                    print(traceback.print_exc())
                    print("--------------------------------------------")
                    news = []
                except:
                    # 謎のエラー発生時。
                    print("--------------------------------------------")
                    print("謎Error in ニュース.")
                    print(traceback.print_exc())
                    print("--------------------------------------------")
                    # raise #Exception補足できないから、もうraiseしない。
                    news = []


            # raiseしたら、Top画面に戻す。
            except:
                print("raised.")
                return render_to_response('kerotan/test_Gmap.html', {'form': form}, RequestContext(request))


            # ---------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------
            # Get route infomation by Ekitan API.
            try:
                print("try ekitan search : ", end="")
                ekitan = Ekitan()
                _, results_filtered = ekitan.norikae_search(s_ido=geocode["start"]["lat"], s_keido=geocode["start"]["lng"], t_ido=geocode["arriv"]["lat"], t_keido=geocode["arriv"]["lng"], )
                print("finished.")
                # print("results_filtered",results_filtered)
                return render_to_response('kerotan/test_Gmap.html', {
                            'form': form, 'route': results_filtered, \
                            'start_latitude': geocode["start"]["lat"], 'start_longitude': geocode["start"]["lng"],\
                            'arriv_latitude': geocode["arriv"]["lat"], 'arriv_longitude': geocode["arriv"]["lng"],\
                            'news': news, 'overview': overview, 'image_company_chart': image_company_chart, 'image_company_building': image_company_building\
                            }, RequestContext(request))

            except FileNotFoundError:
                # APIキーが記述されたファイルの読み込みエラー
                print("--------------------------------------------")
                print("APIキーが記述されたファイルの読み込みエラー")
                print(traceback.print_exc())
                print("--------------------------------------------")
                raise
            except:
                print("--------------------------------------------")
                print(traceback.print_exc())
                print("--------------------------------------------")
                return render_to_response('kerotan/test_Gmap.html', {'form': form}, RequestContext(request))



        # form.is_valid()を満たさない場合
        else:
            return render_to_response('kerotan/test_Gmap.html', {'form': form}, RequestContext(request))
            # return render_to_response('kerotan/test_Gmap.html', {'formset':formset}, RequestContext(request))

    # request.methodがPOSTじゃない場合
    else:
        form = AddressForm()
        return render_to_response('kerotan/test_Gmap.html', {'form': form}, RequestContext(request))
        # return renderrender(RequestContext(request), 'kerotan/test_Gmap.html')
