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

    

class habitat(models.Model):
    cardumen = models.ForeignKey(cardumen, on_delete= models.CASCADE)
    zona = models.ForeignKey(zona, on_delete=models.CASCADE)

    def __str__(self):
            return 'Habitat '+self.cardumen.nombre
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['cardumen', 'zona'], name='habitat_key')
        ]
        
    
