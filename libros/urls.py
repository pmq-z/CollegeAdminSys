from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('nuevo/', views.crear_libro, name='crear_libro'),
    path('editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    
    path('ejemplares/', views.lista_ejemplares, name='lista_ejemplares'),
    path('ejemplares/nuevo/', views.crear_ejemplar, name='crear_ejemplar'),
    path('ejemplares/editar/<int:ejemplar_id>/', views.editar_ejemplar, name='editar_ejemplar'),
    path('ejemplares/eliminar/<int:ejemplar_id>/', views.eliminar_ejemplar, name='eliminar_ejemplar'),
]