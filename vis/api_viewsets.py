# import numpy as np

from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


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
    # Commenting out the vector creation so linting is happy until this is hooked up elsewhere
    # vector = np.asarray([request.data["x"], request.data["y"], request.data["z"]])

    return JsonResponse("Success.", status=200)
