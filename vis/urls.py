from django.urls import path

from . import views
from . import api_viewsets

urlpatterns = [
    # API routes
    path('api/mesh/add_point/', api_viewsets.add_point_to_mesh, name="add point"),
    # UI routes
    path('<path:file_name>/', views.mesh_from_file, name="file"),
    path('', views.mesh_dynamic, name="dynamic"),
]
