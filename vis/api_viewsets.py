import logging

import numpy as np

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.http.response import JsonResponse
from logging import getLogger
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response

from .models import ThreeDimensionalMesh

# Configure the logging level
logging.basicConfig()
logger = getLogger(__name__)

# Get the websocket layer
channel_layer = get_channel_layer()


def send_new_global_mesh():
    if settings.GLOBAL_MESH is None:
        content = {
            "flat_vertices": [],
            "flat_faces": [],
        }
    else:
        content = {
            "flat_vertices": settings.GLOBAL_MESH.get_flat_vertices().tolist(),
            "flat_faces": settings.GLOBAL_MESH.get_flat_faces().tolist(),
        }
    async_to_sync(channel_layer.group_send)("global", {"type": "new_data", "content": content})


@api_view(["PUT"])
@permission_classes((permissions.AllowAny,))
def add_point_to_mesh(request):
    try:
        # Validate data
        if request.content_type != "application/json":
            return JsonResponse({"message": "Bad Request. Content type must be application/json."}, status=400)

        errors = []
        required_params = ["x", "y", "z"]
        for k, v in request.data.items():
            # Make sure all required parameters are present and correct
            if k in required_params:
                if not isinstance(v, (int, float)):
                    errors.append(f"Invalid data type for parameter '{k}'. A number is required.")
                required_params.remove(k)

        for param in required_params:
            errors.append(f"Required parameter '{param}' was not received.")

        if errors:
            return JsonResponse({"message": "Bad Request. Improperly formatted", "errors": errors}, status=400)

        # Everything looks good
        x, y, z = request.data["x"], request.data["y"], request.data["z"]
        vector = np.asarray([[x, y, z]])

        if settings.GLOBAL_MESH is None:
            # We need at least 4 points to build the simplex
            if settings.INITIAL_POINTS is None:
                logger.info("Initialized INITIAL_POINTS with {str([x, y, z])}")
                settings.INITIAL_POINTS = vector
            else:
                logger.info(f"Added {str([x, y, z])} to INITIAL_POINTS")
                settings.INITIAL_POINTS = np.vstack((settings.INITIAL_POINTS, vector))

            if len(settings.INITIAL_POINTS) >= 4:
                try:
                    settings.GLOBAL_MESH = ThreeDimensionalMesh(vertices=settings.INITIAL_POINTS, incremental=True)
                    logger.info("Created global mesh.")
                    send_new_global_mesh()
                except Exception as e:
                    logger.error(f"Could not create global mesh because of:\n{e}"
                                 f"\nAdding point to Initial vertices and will try again")
        else:
            logger.info(f"Added {str([x, y, z])} to global mesh.")
            settings.GLOBAL_MESH.add_vertices(vertices=vector)
            send_new_global_mesh()

        return JsonResponse({"message": f"Success. Added {str([x, y, z])} to mesh."}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({"message": "An error occurred."}, status=500)


@api_view(["DELETE"])
@permission_classes((permissions.AllowAny,))
def clear_mesh(request):
    settings.GLOBAL_MESH = None
    send_new_global_mesh()
    return Response("Mesh cleared", status=200)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_density_map(request):
    if settings.GLOBAL_MESH is not None:
        return JsonResponse(
            {"message": "data enclosed", "data": settings.GLOBAL_MESH.htlm_density_map},
            status=200
        )
    else:
        map_size = ThreeDimensionalMesh.density_map_size()
        return JsonResponse(
            {"message": "no global mesh", "data": [[False] * map_size] * map_size},
            status=201
        )


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_raw_mesh(request):
    if settings.GLOBAL_MESH is None:
        content = {
            "message": "no mesh initializes",
            "flat_vertices": [],
            "flat_faces": [],
        }
        status = 300
    else:
        content = {
            "message": "sent smoothed mesh",
            "flat_vertices": settings.GLOBAL_MESH.get_flat_vertices().tolist(),
            "flat_faces": settings.GLOBAL_MESH.get_flat_faces().tolist(),
        }
        status = 200
    return JsonResponse(
        data=content,
        status=status
    )


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_smooth_mesh(request):
    if settings.GLOBAL_MESH is None:
        content = {
            "message": "no mesh initializes",
            "flat_vertices": [],
            "flat_faces": [],
        }
        status = 300
    else:
        vertices, faces = settings.GLOBAL_MESH.get_smoothed_mesh()
        content = {
            "message": "sent smoothed mesh",
            "flat_vertices": vertices,
            "flat_faces": faces,
        }
        status = 200
    return JsonResponse(
        data=content,
        status=status
    )
