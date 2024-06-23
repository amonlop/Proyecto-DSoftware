from django.contrib import admin
from .models import Cardumen, Zona, Viaje, ViajeCardumen

# Register your models here.
admin.site.register(Cardumen)
admin.site.register(Zona)
admin.site.register(Viaje)
admin.site.register(ViajeCardumen)
