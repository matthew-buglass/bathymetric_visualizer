import numpy as np

from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .models import ThreeDimensionalMesh


@api_view(["PUT"])
@permission_classes((permissions.AllowAny,))
def add_point_to_mesh(request):
    # Validate data
    if request.content_type != "application/json":
        return JsonResponse("Bad Request. Content type must be application/json.", status=400)

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
        return JsonResponse({"text": "Bad Request. Improperly formatted", "errors": errors}, status=400)

    # Everything looks good
    vector = np.asarray([request.data["x"], request.data["y"], request.data["z"]])
    if globals()["GLOBAL_MESH"] is None:
        globals()["GLOBAL_MESH"] = ThreeDimensionalMesh(vertices=vector, incremental=True)
    else:
        globals()["GLOBAL_MESH"].add_vertices(vertices=vector)

    return JsonResponse(f"Success. Added {np.array2string(vector)} to mesh.", status=200)
