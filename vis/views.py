import json

import trimesh
from django.http import HttpResponse
from django.template import loader

import urllib

from vis.utils import flatten


def index(request):
    return HttpResponse("Welcome to the index")


def demo(request):
    # return HttpResponse("Welcome to the demo")
    template = loader.get_template("vis/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def mesh_from_file(request, file_name):
    mesh = trimesh.load(file_name)

    template = loader.get_template("vis/from_file.html")
    context = {
        "flat_vertices": flatten(mesh.vertices),
        "flat_faces": [int(p) for p in flatten(mesh.faces)],
    }
    return HttpResponse(template.render(context, request))

    # return HttpResponse(file_name)
