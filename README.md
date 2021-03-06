# ケロたん
ケロたんは、営業の方向けの経路探索アプリです。
目的地の会社までの経路情報に加え、その会社の概要や、業界のニュースをまとめてお届けします。


#目次
- [本サービスの目的](#本サービスの目的)
- [使い方](#使い方)
- [処理の流れ](#処理の流れ)
- [環境構築](#環境構築)
	- [動作環境](#動作環境)
	- [インストール方法](#インストール方法)
	- [実行方法](#実行方法)
- [バージョン情報](#バージョン情報)


# 本サービスの目的
新人営業が客先訪問の際に必要となる情報を自動で収集、一括で提供します。
これにより、客先への訪問の前準にかかる手間と時間の短縮を目指します。

## 対象ユーザ
* 新人営業
* 客先への訪問の前準備に、必要以上に時間がかかる方


# 使い方
1. メイン画面  
以下がケロたんのメイン画面です。
画面左側の黒いメニューバーに、経路検索のフォームと、経路、会社概要、ニュースの検索結果の表示ボタンがあります。  
画面右側には、各検索結果と経路マップを表示します。
![メイン画面](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_top.png)

1. 経路検索の方法  
画面左の2つの入力フォームにそれぞれ、出発地と目的地の会社名、または住所を入力し、検索ボタンをクリックします。
![経路検索方法](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_input_mokutekiti.png)

1. 検索結果の見方  
経路、目的地の会社概要、関連ニュースの情報が、ブラウザ上に表示されます。
	* 経路  
	検索ボタンをクリックした後か、メニューバーの「経路」ボタンをクリックすると、出発地から目的地までの現在時刻における最適な経路が表示されます。
	![検索結果](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_result_keiro.png)

	* 会社概要の表示  
	「会社概要」のボタンをクリックすると、「目的地」に入力した会社の情報が表示されます。
	![会社概要](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_result_gaiyou.png)

	* ニュースの表示  
	「ニュース」のボタンをクリックすると、「目的地」に入力した会社に関連したニュースが表示されます。
	![ニュース](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/window_result_news.png)

# 処理の流れ
![経路検索方法](https://raw.githubusercontent.com/wiki/tech-sketch/Project_Kerotan/image/flow_of_process.png)
1. ユーザが目的・到着地点の住所または会社名を入力します。検索ボタンをクリックすることで情報がサーバ側（ケロたん）に送信されます。

1. サーバは情報を受け取ると、まずGoogle Maps Geocoding APIを用いて、住所または会社名を緯度経度座標に変換します。  
（※1 v1.0では、社名 → 緯度経度座標への変換は、適切に動作しない可能性があります。[Issues#3](https://github.com/tech-sketch/Project_Kerotan/issues/3))
1. 正しく緯度経度座標を取得できた後、到着地点が社名で入力されていた場合、会社概要と関連ニュースの取得を行います。  
社名で入力されていなかった場合、会社概要と関連ニュースの取得は行いません。
	1. Wikipediaから会社概要を取得します。  
	（※2 v1.0では会社概要の取得機能は未実装のため、あらかじめ作成した辞書データから会社概要を取得します。社名が辞書データに存在しない場合、会社概要の取得は行いません。）
	1. Bing Search APIを用いて、社名に関連するニュースの取得を行います。

1. 駅探ASPを用いて、出発・到着地点の緯度経度座標から最適な経路情報を取得します。

1. （会社概要）、（ニュース）、経路情報をブラウザに送信します。

1. ブラウザはGoogle Maps JavaScript, Directions APIを用いて、地図オブジェクトの生成、地図上に経路情報を反映させます。  
その後、地図と会社概要、ニュース、経路情報をブラウザ上に表示します。

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
ケロたんでは、以下4つのAPIを利用します。
* [駅探ASP](http://go.ekitan.com/service/index.shtml#as1)
* [Bing Search API](https://datamarket.azure.com/dataset/bing/search)
* [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro?hl=ja)
* [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/?hl=ja)

上3つのAPIのライセンスキーは
Project_Kerotan/API/APIkey_write_yaml.py
の中の"key"に、それぞれ記述してください。

Google Maps JavaScript APIのライセンスキーについては、  
Project_Kerotan/project_kerotan/static/js/google_map_api.jsを新たに生成し（.gitignoreされています）、以下を記述してください。
```
document.write("<script src='https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY'></script>");
```
YOUR_API_KEYの部分に、ブラウザキーを記述してください。

記述後、APIkey_wirte_yaml.pyを実行することで、APIキーが記述されたAPI_KEY.yamlが生成されます。
各APIが実行される際、このAPI_KEY.yamlがロードされます。

### Google Maps JavaScript APIキーの生成と認証
Google Maps JavaSctipt APIを使用する際には、万が一APIキーが外部に漏れても他ユーザが使えないようにするために、使用するAPIキーの認証をGoogle API console上で行う必要があります。
（なお、Google API consoleを使用する際にはgoogleアカウントの取得が必要です）

手順  

1. googleアカウントにログインした状態でGoogle API consoleに入ります。（webで調べるとトップに出てきます）  

1. 新規プロジェクトの作成を行います。(プロジェクト名は自由で大丈夫です)  

1. 「Google Maps JavaScript API」を選択します。  

1. 「有効にする」を選択します。  

1. 有効になっていますが、認証情報を生成してくださいと表示されるので、「認証情報に進む」を選択します。  

1. ウェブブラウザ上でAPIを呼び出すため、APIを呼び出す場所を「ウェブブラウザ(Javascript)」に指定し、「必要な認証情報」を選択します。  

1. 「HTTPリファラーからのリクエストを受け入れる」という項目にAPIキーを使用するブラウザのURLを入力します。  
	* ローカルで使用する場合は「http://127.0.0.1:8000」と「http://127.0.0.1:8000/*」を入力してください。  
	* *はワイルドカードとして使用し、選択したURL以下すべてが対象となります。  
	* このHTTPリファラーを設定しない場合、すべてのリクエストを受け付けるようになるため、必ず設定してください。  

1. 「APIキーを生成」を選択して生成されたAPIキーを、先ほどの説明にあったgoogle_map_api.jsに記述してください。  

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


# バージョン情報
* 2015.07.12 v1.0 Release
	*新規作成 
