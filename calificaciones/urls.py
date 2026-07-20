from django.urls import path

from . import views

urlpatterns = [
    # Rutas del Sistema
    path('dashboard/', views.dashboard, name='calificaciones_dashboard'),
    path('curso/<int:curso_id>/calificaciones/', views.grade_entry, name='grade_entry'),
    path('curso/<int:curso_id>/iniciar-firma/', views.iniciar_firma, name='iniciar_firma'),
    path('curso/<int:curso_id>/firmar/', views.digital_signature, name='digital_signature'),
    path('curso/<int:curso_id>/pdf/', views.generar_pdf, name='generar_pdf'),
]