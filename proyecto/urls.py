from django.contrib import admin
from django.urls import path, include
from login import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('registro/', views.registro, name='registro'),
    path('partido/<int:partido_id>/reportar/', views.reportar_partido, name='reportar_partido'),
]
