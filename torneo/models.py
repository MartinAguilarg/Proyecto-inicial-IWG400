from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    capitan = models.ForeignKey(User, on_delete=models.CASCADE)
    elo = models.IntegerField(default=1000)

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    equipo_1 = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_2 = models.ForeignKey(Equipo, related_name='partidos_visita', on_delete=models.CASCADE)
    goles_equipo_1 = models.IntegerField(default=0)
    goles_equipo_2 = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, default='pendiente')
    
    # nuevo campo para calendario
    fecha_programada = models.DateField(null=True, blank=True)
    hora_programada = models.TimeField(null=True, blank=True)
    estado_coordinacion = models.CharField(max_length=20, default='sin_fecha')
    lugar_acordado = models.CharField(max_length=150, null=True, blank=True)
    def __str__(self):
        return f"{self.equipo_1} vs {self.equipo_2}"
class Desafio(models.Model):
    ESTADOS_DESAFIO = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    
    retador = models.ForeignKey(Equipo, related_name='desafios_enviados', on_delete=models.CASCADE)
    retado = models.ForeignKey(Equipo, related_name='desafios_recibidos', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS_DESAFIO, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.retador.nombre} reta a {self.retado.nombre} ({self.estado})"
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20)
    comuna = models.CharField(max_length=50, default="Por definir")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"