from django.urls import path
from . import views


urlpatterns = [
    path(
        "registro/",
        views.registro_usuario,
        name="registro_usuario",
    ),
    path(
        "perfil/",
        views.perfil_usuario,
        name="perfil_usuario",
    ),
]