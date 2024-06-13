from django.db import models
from django.db.models import UniqueConstraint

# Create your models here.
class cardumen(models.Model):
    nombre = models.CharField(primary_key=True, max_length=200)
    def __str__(self):
        return self.nombre

class zona(models.Model):
    coordenadaX = models.IntegerField()
    coordenadaY = models.IntegerField()

    def __str__(self) -> str:
            return 'Zona '+ str(self.pk)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['coordenadaX', 'coordenadaY'], name='zona_key')
        ]
