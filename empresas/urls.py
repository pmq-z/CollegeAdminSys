from django.urls import path

from . import views

urlpatterns = [
    path('', views.empresa_list, name='empresa_list'),
    path('nueva/', views.empresa_create, name='empresa_create'),
]
