import numpy as np

from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .models import ThreeDimensionalMesh


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
            if len(settings.INITIAL_POINTS[0]) == 0:
                settings.INITIAL_POINTS = vector
            else:
                settings.INITIAL_POINTS = np.vstack((settings.INITIAL_POINTS, vector))

            if len(settings.INITIAL_POINTS) == 4:
                settings.GLOBAL_MESH = ThreeDimensionalMesh(vertices=settings.INITIAL_POINTS, incremental=True)
        else:
            settings.GLOBAL_MESH.add_vertices(vertices=vector)

        return JsonResponse({"message": f"Success. Added {str([x, y, z])} to mesh."}, status=200)
    except Exception:
        return JsonResponse({"message": f"An error occurred."}, status=500)
