from django.urls import path

from . import views

urlpatterns = [
    path('', views.billetera_list, name='billetera_list'),
    path('nuevo/', views.movimiento_create, name='movimiento_create'),
]
