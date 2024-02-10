from django.http import HttpResponse
from django.template import loader

from vis.models import ThreeDimensionalMesh

GLOBAL_MESH: ThreeDimensionalMesh = None


def mesh_from_file(request, file_name):
    try:
        mesh = ThreeDimensionalMesh.load_from_file(file_name)
    except ValueError:
        return HttpResponse(f"The file '{file_name}' was not found")

    template = loader.get_template("vis/from_file.html")
    context = {
        "flat_vertices": list(mesh.get_flat_vertices()),
        "flat_faces": list(mesh.get_flat_faces()),
    }
    return HttpResponse(template.render(context, request))


def mesh_dynamic(request):
    template = loader.get_template("vis/from_file.html")

    if GLOBAL_MESH is not None:
        context = {
            "flat_vertices": list(GLOBAL_MESH.get_flat_vertices()),
            "flat_faces": list(GLOBAL_MESH.get_flat_faces()),
        }
    else:
        context = {
            "flat_vertices": [],
            "flat_faces": [],
        }

    return HttpResponse(template.render(context, request))
