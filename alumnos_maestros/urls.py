from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('alumnos/', views.alumno_list, name='alumno_list'),
    path('alumnos/nuevo/', views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.alumno_update, name='alumno_update'),
    path('alumnos/<int:pk>/desactivar/', views.alumno_deactivate, name='alumno_deactivate'),
    path('maestros/', views.maestro_list, name='maestro_list'),
    path('maestros/nuevo/', views.maestro_create, name='maestro_create'),
    path('maestros/<int:pk>/editar/', views.maestro_update, name='maestro_update'),
    path('maestros/<int:pk>/desactivar/', views.maestro_deactivate, name='maestro_deactivate'),
    path('materias/', views.materia_list, name='materia_list'),
    path('materias/nueva/', views.materia_create, name='materia_create'),
    path('materias/<int:pk>/editar/', views.materia_update, name='materia_update'),
    path('materias/<int:pk>/desactivar/', views.materia_deactivate, name='materia_deactivate'),
    path('inscripciones/', views.inscripcion_list, name='inscripcion_list'),
    path('inscripciones/nueva/', views.inscripcion_create, name='inscripcion_create'),
    path('inscripciones/<int:pk>/desactivar/', views.inscripcion_deactivate, name='inscripcion_deactivate'),
]
