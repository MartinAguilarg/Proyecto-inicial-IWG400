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
    path('perfil/<int:equipo_id>/', views.perfil_equipo, name='perfil_equipo'),
    path('ranking/', views.ranking, name='ranking'),
    path('mi_perfil/', views.mi_perfil, name='mi_perfil'),
    path('calendario/', views.calendario, name='calendario'),
    path('coordinar/<int:partido_id>/', views.proponer_horario, name='proponer_horario'),
    path('coordinacion/', views.coordinacion, name='coordinacion'),
    path('coordinar/<int:partido_id>/', views.proponer_horario, name='proponer_horario'),
    path('calendario/', views.calendario, name='calendario'),
]
