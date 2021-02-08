# ブログ作成までのチュートリアル
[Django Tutorial 攻略](https://www.youtube.com/watch?v=nS41IkL13QE&list=PLuCS8p0T7ozK4Ne1e5eAVG2R5Gbs1naix)で学んだ内容のメモ


<br>


# 基本操作
1. [開発環境構築](#anchor1)
2. [プロジェクトを新たにスタートする](#anchor2)
3. [開発サーバーを起動する](#anchor3)
4. [新たにアプリケーションを追加する](#anchor4)
5. [appのWebページを追加する](#anchor5)
6. [Webページを複数作る](#anchor6) HTML,CSSの使い方は説明を省く
7. [HTMLに変数を用いる](#anchor7)
8. [静的ファイルを配置する](#anchor8)
9. [Herokuへの公開](#anchor9)
10. [データベース接続](#anchor10)

<br>


<a id="anchor1"></a>

# 1 開発環境構築
```bash
$ docker-compose up -d
```
<br>


<a id="anchor2"></a>

# 2 プロジェクトを新たにスタートする
```bash
$ django-admin startproject project_name
```
<br>


<a id="anchor3"></a>

# 3 開発サーバーを起動する
```bash
$ python manage.py runserver
```
<br>


<a id="anchor4"></a>

# 4 新たにアプリケーションを追加する
```bash
$ python manage.py startapp app_name
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
    'app_name', # ここにapp名を追加する
]
```
<br>


<a id="anchor5"></a>

# 5 appのWebページを追加する
1. app_nameのフォルダ内にて```templates```フォルダを作成
2. ```templates```フォルダ内に```index.html```(例)を作成
3. app_nameのフォルダ内の```views.py```に以下を記載(例)
```python
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html' # 先ほど作成したhtmlファイルの名前
```
4. app_nameフォルダ内の```urls.py```でviewとURLを結びつける記載をする(```urls.py```がない場合は新規作成)
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
5. プロジェクトフォルダ内(/project_name/project_name)の```urls.py```も編集する
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')) # トップページにアクセスしたらwebsiteフォルダ内のurlsを見にいく
]
```
1~5の設定によりユーザーがトップページにアクセスすると  
* /app_name/website/urls.pyに飛ばされる  
* /app_name/website/views.pyに飛ばされる
* /app_name/website/templates/index.htmlに飛ばされる

<br>


<a id="anchor6"></a>

# 6 Webページを複数作る
Webページ(リンク)を複数作りたい場合は、  
* app_nameフォルダの```views.py```のクラスを新たに設計する
* app_nameフォルダの```urls.py```に新たにurlpatternsを追加する

の２つを行えばOK. プロジェクトフォルダの```urls.py```は修正する必要がないので注意  
<br>
/app_name/views.pyにて

```python
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'
```
<br>

/app_name/urls.pyにて  

```python
from django.urls import path

from .views import IndexView, AboutView

urlpatterns = [
    path('', IndexView.as_view()),
    path('about/', AboutView.as_view()), # /about/でapp_name/views.pyのAboutView(TemplateView)を実行し, templates/about.htmlを参照する
]
```
のように追記すれば良い

<br>


<a id="anchor7"></a>

# 7 HTMLに変数を用いる
app_nameフォルダの```views.py```のクラスに、```get_context_data```メソッドを作成することでHTML内で変数を用いることが可能になる.  
```TemplateView```を継承した```super().get_context_data()```メソッドによって得られたオブジェクトはPythonのリスト型であり, これにKeyとValueを設定することで, HTMLからKeyを用いて呼び出し可能. ```views.py```の書き方は以下を参照.クラス毎に用いる変数をそれぞれ定義する必要がある.  


```python
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt['username'] = 'hoge' #ここでctxtのkeyとvalueを設定すると、このkeyをhtmlファイルの変数として用いることができる
        return ctxt


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt['n_services'] = 123456789
        ctxt['skills'] = [ # listで渡してHTML内でforでitemを列挙することも可能
            'Python',
            'C++',
            'Javascript',
        ]
        return ctxt
```
<br>

<a id="anchor8"></a>

# 8 静的ファイルを配置する
アプリを公開するときは必ず```settings.py```のデバッグを```DEBUG = False```のようにオフにしなければならない. しかし, このままではブラウザで画像を読み込めない.従って以下のツールで対処する  
<br>
1.

whitenoiseをインストールする
```bash
$ pip install whitenoise
```
<br>
2.  

次に, ```settings.py```の末尾に以下の記述を加える  
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
また, ```settings.py```の```MIDDLEWARE ```リストに```'whitenoise.middleware.WhiteNoiseMiddleware'```を追加する  
<br>
3.

次に, プロジェクトフォルダと同階層に```static_root```フォルダを作成し, ここにDjangoで扱っている静的ファイルを全てコピーしなければならない. 以下のコマンドで一括にフォルダ作成からコピーが行える.  
```bash
$ python manage.py collectstatic
```
<br>


<a id="anchor9"></a>

# 9 Herokuを用いたデプロイ

① [Herokuの公式サイト](https://dashboard.heroku.com/)でユーザー登録とappの新規作成を行う.  

② Herokuをインストールする
```bash
$ brew tap heroku/brew && brew install heroku
```

③ Herokuへのデプロイ準備  
DjangoアプリケーションをHerokでデプロイするには新たに２つのファイルが必要. 一つはプロジェクトに用いる全ライブラリを記述した```requirements.txt```, もう一つは```Procfile```.  
これらのファイルがアプリのルートに存在するとHerokuはデプロイするアプリケーションの言語をPythonだと自動認識してくれる.
<br>

*requirements.txt*
```
django
whitenoise
requests
numpy
scipy
pandas
jupyter
``` 
<br>

*Procfile*
```
web: gunicorn django_website2.wsgi
```
<br>

③ デプロイ用のGitHubリポジトリを新たに作成  
次に, **アプリケーションの**GitHubリポジトリを別に作成.以下のようなリポジトリを想定. 以下のGitHubリポジトリとHerokuを同期させることでHerokuを用いたデプロイが可能. 
```
|-django_website2
|       |_...
|       |_...
|       |_...
|
|-website2
|    |_...
|    |_...
|    |_...
|
|-Procfile
|-equirements.txt
|-manage.py
```
<br>

④ ③で作成したGitHubリポジトリを別ディレクトリにクローン  
　　

⑤ アプリケーションのリポジトリの直下で以下のコマンドを実行
```
$ heroku create
$ git push heroku main
$ heroku ps:scale web=1
$ heroku open
```
詳しくは[Herokuの公式チュートリアル](https://devcenter.heroku.com/ja/articles/getting-started-with-python#-4)で.
<br>
<br>

<a id="anchor10"></a>

# 10 データベース接続

## Sqlite3と接続  
<br>

djangoがデフォルトで持っているsqliteのデータベースの動作確認.  
15行ほどログが出力されて成功すればOK.
```
$ python manage.py migrate
```
**試しにスーパーユーザー（管理者）を作成してみよう**  
ユーザー名、メール、パスワードを聞かれるので答えると作成されます。
```
$ python manage.py createsuperuser
```
**管理者画面に入る**  
開発用サーバーを立ち上げてURLの末尾に```/admin/```で管理画面に入れる.
<br>
<br>

## MySQLと接続
---工事中---


