# チャットボット

## 概要
PythonのフレームワークDjangoを利用したチャットボットです

## 環境
- python 3.7
- Django 2.1
- Janome 0.3.9
- PyMysql 0.8.0
- Mysql 14.14
※ Django等はpipまたはPycharmでインストールします。
  Pycharmを使う場合はcondaを利用することができません。

## 実行方法
PyCharmで実行環境を構築すると実行が簡単ですが、
ターミナル上での実行方法を記述します。

`mysql.server start`


`python /作業ディレクトリ/manage.py runserver`
サーバーを起動できたら http://127.0.0.1:8000/chat_app/ にアクセスします。
