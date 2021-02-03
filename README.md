# WebDrugManager
LINEBotと連帯した服薬管理(お薬手帳)Webアプリケーションを作る企画.  
服薬管理を行うLINEBotは別リポジトリで開発中(非公開).
<br>
<br>

# 開発手順
1. [Django Tutorial 攻略](https://www.youtube.com/watch?v=nS41IkL13QE&list=PLuCS8p0T7ozK4Ne1e5eAVG2R5Gbs1naix)
2. ログイン機能の実装  
3. ユーザ毎に異なるページを表示する機能を実装  
4. LINEでログインできるようにする  
5. 服薬カレンダーをユーザー毎に表示する機能を実装  
6. LINEBOTのリマインド機能に対するreplyをWeb服薬カレンダーに反映

<br>

# 開発環境構築
```bash
$ docker-compose up -d
```
<br>

# 基本操作
**プロジェクトを新たにスタートする**
```bash
$ django-admin startproject project_name
```
<br>

**開発サーバーを起動する**
```bash
$ python manage.py runserver
```
<br>

**新たにアプリケーションを追加する** 
```bash
$ python manage.py startapp appN
```
/project_name/project_name/settings.pyを編集する
```python:settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appN', # ここにapp名を追加する
]
```
<br>

**appのWebページを追加**
1. appのフォルダ内にて```templates```フォルダを作成
2. ```templates```フォルダ内にhtmlファイルを作成
3. appのフォルダ内の```views.py```に以下を記載(例)
```python
from django.veiws.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'html_file_name.html' # 先ほど作成したhtmlファイルの名前
```
4. appフォルダ内の```urls.py```でviewとURLを結びつける記載をする(```urls.py```がない場合は新規作成)
```python
from django.urls import path
from .views import IndexView # 先ほど作成したviews.pyからインポート


urlpatterns = [
    path(
        '', # 何も描かない場合はトップページに飛ぶ
        IndexView.as_view()
        ),
]
```
5. プロジェクトの方の```urls.py```も編集する
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')) # トップページにアクセスしたらwebsiteフォルダ内のurlsを見にいく
]
```