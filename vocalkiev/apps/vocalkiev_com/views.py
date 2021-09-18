from django.template import loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template('vocalkiev_com/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
