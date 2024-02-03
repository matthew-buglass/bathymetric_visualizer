from django.urls import path

from . import views

urlpatterns = [
    path('<path:file_name>/', views.mesh_from_file, name="file"),
]
