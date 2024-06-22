from django.db import models
from django.db.models import UniqueConstraint

# Create your models here.
class cardumen(models.Model):
    nombre = models.CharField(primary_key=True, max_length=200)
    def __str__(self):
        return self.nombre

class zona(models.Model):
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
