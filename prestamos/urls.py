from django.urls import path
from . import views


urlpatterns = [
    path('solicitar/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitudes/rechazar/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),

    path('registrar/', views.registrar_prestamo, name='registrar_prestamo'),
    path('activos/', views.prestamos_activos, name='prestamos_activos'),
    path('devolver/<int:prestamo_id>/', views.registrar_devolucion, name='registrar_devolucion'),
]