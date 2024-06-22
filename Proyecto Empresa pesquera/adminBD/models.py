from django.db import models
from django.db.models import UniqueConstraint
from datetime import datetime

# Create your models here.
class Cardumen(models.Model):
    nombre = models.CharField(primary_key=True, max_length=200)
    profundidad_min = models.IntegerField()
    profundidad_max = models.IntegerField()
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    x_min = models.IntegerField()
    x_max = models.IntegerField()
    y_min = models.IntegerField()
    y_max = models.IntegerField()

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    coordenadaX_1 = models.IntegerField()
    coordenadaX_2 = models.IntegerField()
    coordenadaY_1 = models.IntegerField()
    coordenadaY_2 = models.IntegerField()

    def __str__(self) -> str:
            return 'Zona '+ str(self.pk)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['coordenadaX', 'coordenadaY'], name='zona_key')
        ]


class Viaje(models.Model):
    nombre_viaje = models.CharField(max_length=200)
    fecha_salida = models.DateField()
    fecha_llegada = models.DateField()
    es_viaje_exitoso = models.IntegerField()

    def __str__(self) -> str:
         return "Viaje" + str(self.pk)


    def duracion_viaje():
        return (self.fecha_llegada - self.fecha_salida).days

