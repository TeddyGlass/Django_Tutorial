from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post

## viewはtemplate_name(表示先のhtmlのファイル名≠URL)を指定する＆表示する変数を指定する
## urlsはviewとurlを紐付ける(これで間接的にhtmlとurlと表示したい内容が融合する)
## 汎用ビューを用いると、template_nameが自動的に決定してしまうことがあるので注意。templatesのHTMLファイルの名前を対応させなければならない


# ListViewは一覧を簡単に作るためのView
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post


# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post


# CreateViewは新規作成画面を簡単に作るためのView
class Create(CreateView):
    model = Post
    # 編集対象にするフィールド名(models.pyに書いてあるPostの中にあるフィールドの名前に対応する)
    fields = ["title", "body", "category", "tags"]


class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]


class Delete(DeleteView):
    model = Post
    # 削除したあとに移動する先（トップページ）
    success_url = "/"
