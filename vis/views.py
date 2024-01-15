from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Welcome to the index")


def demo(request):
    template = loader.get_template("bathymetric_visualizer/index.html")
    context = {}
    return HttpResponse(template.render(context, request))
