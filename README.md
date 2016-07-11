# ケロたん
ケロたんは、営業の方向けの経路探索アプリです。
目的地の会社までの経路情報に加え、その会社の概要や、業界のニュースをまとめてお届けします。


#目次
- [本サービスの目的](#本サービスの目的)
- [使い方](#使い方)
- [環境構築](#環境構築)
	- [動作環境](#動作環境)
	- [インストール方法](#インストール方法)
		- [モジュールのインストール](#モジュールのインストール)
		- [外部APIのライセンスキー設定](#外部APIのライセンスキー設定)
	- [実行方法](#実行方法)
		- [データベースの設定](#データベースの設定)
		- [サーバの起動](#サーバの起動)
- [](#)


# 本サービスの目的
新人営業が客先訪問の際に必要となる情報を自動で収集、一括で提供します。
これにより、客先への訪問の前準にかかる手間と時間の短縮を目指します。

## 対象ユーザ
* 新人営業
* 客先への訪問の前準備に、必要以上に時間がかかる方


# 使い方
1. メイン画面
以下がケロたんのメイン画面です。
![メイン画面](画像のパス)

1. 経路検索の方法
![経路検索方法](画像のパス)

1. 検索結果の見方
![検索結果](画像のパス)

1. 会社概要の表示
![会社概要](画像のパス)

1. ニュースの表示
![ニュース](画像のパス)


# 環境構築
## 動作環境
動作環境は以下の通りです。
* OS：Windows 7 or CentOS 7
* 言語：Python 3．5.1
* DB：sqlite3


##インストール方法
アプリケーション実行に必要なモジュールのインストール方法、利用する外部APIのライセンスキーの設定方法について説明します。

###モジュールのインストール
ケロたんを動作させるために必要なモジュールは、以下のコマンドでインストールできます。
```shell
$ pip install -r requirements.txt
```

###外部APIのライセンスキーの設定
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


##実行方法
データベースの設定、サーバの起動方法について説明します。

###データベースの設定
Project_Kerotan/project_kerotan/project_kerotan/settings.pyにてデータベースの設定を行います。
以下に、sqlite3の設定例を示します。
（なおバージョン1.0においては、データベースは使用していません。）
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


###サーバの起動
以下のコマンドでサーバを起動します。
```shell
$ cd Project_Kerotan/project_kerotan
$ python manage.py runserver
```
サーバ起動後、Webブラウザでhttp://127.0.0.1:8000/ にアクセスします。


