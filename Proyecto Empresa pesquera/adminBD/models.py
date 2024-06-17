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
    coordenadaX = models.IntegerField()
    coordenadaY = models.IntegerField()
    profundidad = models.IntegerField()
    temperatura = models.IntegerField()

    def __str__(self) -> str:
            return 'Zona '+ str(self.pk)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['coordenadaX', 'coordenadaY'], name='zona_key')
        ]


class Viaje(models.Model):
    fecha_salida = models.DateField()
    fecha_llegada = models.DateField()
    es_viaje_exitoso = models.IntegerField()

    def __str__(self) -> str:
         return "Viaje" + str(self.pk)


    def duracion_viaje():
        return (self.fecha_llegada - self.fecha_salida).days


class Embarcacion(models.Model):
    nombre = models.CharField()
    capacidad_tripulacion = models.IntegerField()
    capacidad_bodega = models.IntegerField() #cuantos kls de mercadería pueden almacenar


    def __str__(self) -> str:
         return "Embarcación" + str(self.pk)
