from django.veiws.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
