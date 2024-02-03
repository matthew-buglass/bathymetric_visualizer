from django.urls import path

from . import views

urlpatterns = [
    path('1/<path:file_name>/', views.mesh_from_file, name="file"),
    path('2/<path:file_name>/', views.mesh_from_file_2, name="file2"),
]
