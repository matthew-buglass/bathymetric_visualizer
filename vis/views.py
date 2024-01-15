from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Welcome to the index")


def demo(request):
    # return HttpResponse("Welcome to the demo")
    template = loader.get_template("vis/index.html")
    context = {}
    return HttpResponse(template.render(context, request))
