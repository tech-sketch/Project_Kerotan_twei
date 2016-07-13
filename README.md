# ケロたん
ケロたんは、営業の方向けの経路探索アプリです。
目的地の会社までの経路情報に加え、その会社の概要や、業界のニュースをまとめてお届けします。


#目次
- [本サービスの目的](#本サービスの目的)
- [使い方](#使い方)
- [仕様詳細](#仕様詳細)
- [環境構築](#環境構築)
	- [動作環境](#動作環境)
	- [インストール方法](#インストール方法)
	- [実行方法](#実行方法)
- [今後の課題](#今後の課題)


# 本サービスの目的
新人営業が客先訪問の際に必要となる情報を自動で収集、一括で提供します。
これにより、客先への訪問の前準にかかる手間と時間の短縮を目指します。

## 対象ユーザ
* 新人営業
* 客先への訪問の前準備に、必要以上に時間がかかる方


# 使い方
1. メイン画面  
以下がケロたんのメイン画面です。
画面左側に、経路検索とその結果を表示します。
画面右側に、経路検索結果と連動したマップを表示します。
![メイン画面](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_top.png)

1. 経路検索の方法  
画面左の2つの入力フォームにそれぞれ、出発地と目的地の住所を入力し、検索ボタンをクリックします。
![経路検索方法](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_input_mokutekiti.png)

1. 検索結果の見方  
フォームに入力された内容から、サーバ側が経路情報などを検索し、ブラウザ上に表示します。
	* 経路  
	入力フォームの下側に経路検索の結果が表示されます。
	現在時刻における出発地点と到着地点までの最適な経路が表示されます。
	![検索結果](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_result_keiro.png)

	* 会社概要の表示  
	「会社概要」のタブをクリックすると、入力フォームの内「目的地」に設定した場所の情報が表示されます。
	![会社概要](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_gaiyou.png)

	* ニュースの表示  
	「ニュース」のタブをクリックすると、同じく「目的地」に関連したニュースが表示されます。
	![ニュース](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_news.png)

# 処理の流れ
![経路検索方法](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/flow_of_process.png)
1. ユーザが目的・到着地点の社名または住所の情報を入力します。
検索ボタンをクリックすることで情報がサーバ側（ケロたん）に送信されます。
1. サーバは情報を受け取ると、まずGoogle Maps Geocoding APIを用いて、社名または住所を緯度経度座標に変換します。
（社名 → 緯度経度座標への変換は、適切に動作しない可能性があります。[Issues#3](https://github.com/tech-sketch/Project_Kerotan/issues/3))
1. 正しく緯度経度座標を取得できた後、到着地点が社名で入力されていた場合、会社概要と関連ニュースの取得を行います。社名で入力されていなかった場合、会社概要と関連ニュースの取得は行いません。
	1. v1.0では会社概要の取得機能は未実装のため、あらかじめ作成した辞書データから会社概要を取得します。
	社名が辞書データに存在しない場合、会社概要の取得は行いません。
	1. Bing Search APIを用いて、社名に関連するニュースの取得を行います。
1. 駅探ASPを用いて、出発・到着地点の緯度経度座標から最適な経路情報を取得します。
1. （会社概要）、（ニュース）、経路情報をブラウザに送信します。
1. ブラウザはGoogle Maps JavaScript, Directions APIを用いて、地図オブジェクトの生成、地図上に経路情報を反映させます。
その後、受け取った会社概要、ニュース、経路情報、地図をブラウザ上に表示します。

# 環境構築
## 動作環境
動作環境は以下の通りです。
* OS：Windows 7 or CentOS 7
* 言語：Python 3．5.1
* DB：sqlite3


## インストール方法
アプリケーション実行に必要なモジュールのインストール方法、利用する外部APIのライセンスキーの設定方法について説明します。

### モジュールのインストール
ケロたんを動作させるために必要なモジュールは、以下のコマンドでインストールできます。
```
shell
$ pip install -r requirements.txt
```

### 外部APIのライセンスキーの設定
ケロたんでは、以下5つのAPIを利用します。
* [駅探ASP](http://go.ekitan.com/service/index.shtml#as1)
* [Bing Search API](https://datamarket.azure.com/dataset/bing/search)
* [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/?hl=ja)
* [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/?hl=ja)
* [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro?hl=ja)

各APIのライセンスキーは
Project_Kerotan/API/APIkey_write_yaml.py
の中の"key"に、それぞれ記述してください。
なお、Google Maps JavaScript API、Google Maps Directions APIに関してはライセンスキーは不要です。
記述後、APIkey_wirte_yaml.pyを実行することで、APIキーが記述されたAPI_KEY.yamlが生成されます。
各APIが実行される際、このAPI_KEY.yamlがロードされます。

## 実行方法
データベースの設定、サーバの起動方法について説明します。

### データベースの設定
Project_Kerotan/project_kerotan/project_kerotan/settings.pyにてデータベースの設定を行います。
以下に、sqlite3の設定例を示します。
（なおバージョン1.0においては、データベース設定は行っていますが、使用はしていません。）
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
設定が完了したら、以下を実行して、マイグレーションを行います。
```
$ cd Project_Kerotan/project_kerotan
$ python manage.py makemigrations
$ python manage.py migrate
```


### サーバの起動
以下のコマンドでサーバを起動します。
```shell
$ cd Project_Kerotan/project_kerotan
$ python manage.py runserver
```
サーバ起動後、Webブラウザでhttp://127.0.0.1:8000/ にアクセスします。

# 今後の課題
##経路検索結果とGoogleMapDirectionsの検索結果のGeocodeのズレ
経路検索で用いるgeocodeとマップ上に表示するgeocodeが異なるために、
最寄駅から目的地までの経路に不必要な経路が存在する。

## 会社概要の取得機能
会社概要を取得する機能が未実装である。
バージョン1.0では、あらかじめ設定した会社の概要しか表示することができない。
実装方法としては、以下が考えられる。
* WikipediaのAPIの利用
* YahooFinanceなど無償で企業情報を提供するWebサービスからスクレイピング

## 社名から住所への変換
出発地・目的地の入力フォームには、会社名ではなく住所の入力が必要となっている。
会社名から住所への変換機能は未実装である。
実装方法として、会社概要の取得機能の実装方法に加え、Google Mapsの機能の利用が考えられる。

# 今後の追加機能
* 議事録の管理・表示機能
* ログイン機能
* 入力履歴の保存
* お気に入り登録
* その他、UIなどユーザビリティ向上

# バージョン情報
* 2015.07.12 v1.0 Release
	*新規作成 
