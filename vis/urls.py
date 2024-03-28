from django.urls import path

from . import views
from . import api_viewsets

urlpatterns = [
    # API routes
    path('api/mesh/add_point/', api_viewsets.add_point_to_mesh, name="add point"),
    path('api/mesh/clear/', api_viewsets.clear_mesh, name="clear global mesh"),
    path('api/mesh/densitymap/', api_viewsets.get_density_map, name="get density map"),
    path('api/mesh/raw/', api_viewsets.get_raw_mesh, name="get density map"),
    path('api/mesh/smooth/', api_viewsets.get_smooth_mesh, name="get density map"),
    # UI routes
    path('', views.mesh_dynamic, name="dynamic"),
]
