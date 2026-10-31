from django.db import models
from django.contrib.auth.models import User

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    capitan = models.ForeignKey(User, on_delete=models.CASCADE)
    elo = models.IntegerField(default=1000)

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('esperando_c2', 'Esperando confirmación del Capitán 2'),
        ('confirmado', 'Confirmado'),
        ('disputa', 'En Disputa'),
    ]

    equipo_1 = models.ForeignKey(Equipo, related_name='partidos_1', on_delete=models.CASCADE)
    equipo_2 = models.ForeignKey(Equipo, related_name='partidos_2', on_delete=models.CASCADE)
    
    # Resultado oficial 
    goles_equipo_1 = models.IntegerField(null=True, blank=True)
    goles_equipo_2 = models.IntegerField(null=True, blank=True)
    
    # Reporte del Capitán 1
    goles_1_c1 = models.IntegerField(null=True, blank=True)
    goles_2_c1 = models.IntegerField(null=True, blank=True)
    
    # Reporte del Capitán 2
    goles_1_c2 = models.IntegerField(null=True, blank=True)
    goles_2_c2 = models.IntegerField(null=True, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.equipo_1} vs {self.equipo_2} ({self.estado})"
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