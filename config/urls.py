"""URL configuration for the unified sistema_escolar project."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path('healthz/', views.healthcheck, name='healthcheck'),

    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', views.home, name='home'),

    path('academico/', include('alumnos_maestros.urls')),
    path('calificaciones/', include('calificaciones.urls')),
    path('horarios/', include('horarios.urls')),
    path('empresas/', include('empresas.urls')),
    path('billetera/', include('billetera.urls')),

     # Biblioteca
    path('usuarios/', include('usuarios.urls')),
    path('libros/', include('libros.urls')),
    path('prestamos/', include('prestamos.urls')),
]
