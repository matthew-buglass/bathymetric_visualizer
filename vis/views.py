from django.conf import settings
from django.http import HttpResponse
from django.template import loader

from vis.models import ThreeDimensionalMesh


def mesh_from_file(request, file_name):
    try:
        mesh = ThreeDimensionalMesh.load_from_file(file_name)
    except ValueError:
        return HttpResponse(f"The file '{file_name}' was not found")

    template = loader.get_template("vis/from_file.html")
    context = {
        "flat_vertices": mesh.get_flat_vertices().tolist(),
        "flat_faces": mesh.get_flat_faces().tolist(),
    }
    return HttpResponse(template.render(context, request))


def mesh_dynamic(request):
    template = loader.get_template("vis/dynamic.html")

    if settings.GLOBAL_MESH is not None:
        context = {
        "flat_vertices": settings.GLOBAL_MESH.get_flat_vertices().tolist(),
        "flat_faces": settings.GLOBAL_MESH.get_flat_faces().tolist(),
    }
    else:
        context = {
            "flat_vertices": [],
            "flat_faces": [],
        }

    return HttpResponse(template.render(context, request))
