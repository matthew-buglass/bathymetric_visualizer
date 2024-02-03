from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(["PUT"])
@permission_classes((permissions.AllowAny,))
def add_point_to_mesh(request):
    print("You've posted")
    return JsonResponse({"text": "Hello World"}, status=200)

