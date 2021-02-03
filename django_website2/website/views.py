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
        return ctxt

