from django.urls import path
from . import views

urlpatterns = [

    # Página principal
    path('', views.index, name='horarios_index'),

    # Editar horario
    path('editar/<int:id>/', views.editar, name='editar'),

    # Eliminar horario
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),

]