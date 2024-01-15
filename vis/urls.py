from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('demo/', views.demo, name="demo"),
    path('file/<path:file_name>/', views.mesh_from_file, name="file"),
]
