# ケロたん
ケロたんは、営業の方向けの経路探索アプリです。
目的地の会社までの経路情報に加え、その会社の概要や、業界のニュースをまとめてお届けします。

#目次
- [](#) 
- [](#) 
- [](#) 
- [](#) 
- [](#) 

##動作環境
動作環境は以下の通りです。
* OS：Windows 7 or CentOS 7
* 言語：Python 3．5.1
* DB：sqlite3

##インストール方法
アプリケーション実行に必要なモジュールのインストール方法、利用する外部APIのライセンスキーの設定方法について説明します。
###モジュールのインストール
ケロたんを動作させるために必要なモジュールは以下のコマンドでインストールできます。
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
データベースの設定、ポートの設定、サーバの起動方法について説明します。
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
$ python manage.py makemigrations
$ python manage.py migrate
```

##サーバの起動
以下のコマンドでサーバを起動します。
```
$ python app.py
```
サーバ起動後、Webブラウザで、http://127.0.0.1:8000/ にアクセスします。


