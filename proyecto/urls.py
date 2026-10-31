from django.contrib import admin
from django.urls import path, include
from torneo import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('registro/', views.registro, name='registro'),
    path('partido/<int:partido_id>/reportar/', views.reportar_partido, name='reportar_partido'),
    path('radar/', views.radar_desafios, name='radar'),
    path('desafio/enviar/<int:retado_id>/', views.enviar_desafio, name='enviar_desafio'),
    path('bandeja/', views.bandeja_desafios, name='bandeja_desafios'),
    path('desafio/responder/<int:desafio_id>/<str:accion>/', views.responder_desafio, name='responder_desafio'),
]
