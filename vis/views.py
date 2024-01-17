import trimesh
from django.http import HttpResponse
from django.template import loader

from vis.utils import flatten


def mesh_from_file(request, file_name):
    try:
        mesh = trimesh.load(file_name)
    except ValueError:
        return HttpResponse(f"The file '{file_name}' was not found")

    template = loader.get_template("vis/from_file.html")
    context = {
        "flat_vertices": flatten(mesh.vertices),
        "flat_faces": flatten(mesh.faces, int),
    }
    return HttpResponse(template.render(context, request))

    # return HttpResponse(file_name)
