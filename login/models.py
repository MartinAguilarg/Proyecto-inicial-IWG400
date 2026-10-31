from django.db import models
from django.contrib.auth.models import User

class Equipo(models.Model):
    capitan = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    elo = models.IntegerField(default=1000)  # Todos 
    puntualidad = models.IntegerField(default=100)

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    equipo_1 = models.ForeignKey(Equipo, related_name='partidos_locales', on_delete=models.CASCADE)
    equipo_2 = models.ForeignKey(Equipo, related_name='partidos_visitantes', on_delete=models.CASCADE)
    goles_equipo_1 = models.IntegerField(null=True, blank=True)
    goles_equipo_2 = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pendiente') # Pendiente, Confirmado, Disputa

    def __str__(self):
        return f"{self.equipo_1} vs {self.equipo_2}"