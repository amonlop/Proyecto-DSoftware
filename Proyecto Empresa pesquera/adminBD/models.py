from django.db import models

# Create your models here.
class Cardumen(models.Model):
    especie = models.CharField(primary_key=True, max_length=200)
    profundidad_min = models.IntegerField()
    profundidad_max = models.IntegerField()
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    x_min = models.IntegerField()
    x_max = models.IntegerField()
    y_min = models.IntegerField()
    y_max = models.IntegerField()

    def __str__(self):
        return self.especie



class Zona(models.Model):
    x_min = models.IntegerField()
    x_max = models.IntegerField()
    y_min = models.IntegerField()
    y_max = models.IntegerField()
    profundidad = models.IntegerField()
    temperatura = models.IntegerField()

    def __str__(self) -> str:
            return 'Zona ' + str(self.x_min) + "\u2191 " + str(self.y_min) + "\u2191 " + str(self.profundidad) + "m " + str(self.temperatura) + "°C"


class Viaje(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    fecha_salida = models.DateField()
    fecha_llegada = models.DateField()
    es_viaje_exitoso = models.BooleanField()

    def __str__(self) -> str:
         return "Viaje " + str(self.pk) + " " + str(self.zona.x_min) + "\u2191 "+ str(self.zona.y_min) + "\u2191" + str(self.zona.profundidad) + "m " + str(self.zona.temperatura) + "°C"

class ViajeCardumen(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    cardumen = models.ForeignKey(Cardumen, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Viaje " + str(self.viaje.pk) + " | Cardumen " + str(self.cardumen.especie)