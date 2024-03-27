from django.urls import path

from . import views
from . import api_viewsets

urlpatterns = [
    # API routes
    path('api/mesh/add_point/', api_viewsets.add_point_to_mesh, name="add point"),
    path('api/mesh/clear/', api_viewsets.clear_mesh, name="clear global mesh"),
    path('api/mesh/densitymap/', api_viewsets.get_density_map, name="get density map"),
    # UI routes
    # path('<path:file_name>/', views.mesh_from_file, name="file"),
    path('', views.mesh_dynamic, name="dynamic"),
]
