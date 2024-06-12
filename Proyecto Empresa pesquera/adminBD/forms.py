from django import forms

class crearCardumen(forms.Form):
    nombre = forms.CharField(label="Nombre cardumen", max_length=200)

class ingresarCoordenadas(forms.Form):
    coordenadaX = forms.IntegerField(label="coordenada X")
    coordenadaY = forms.IntegerField(label="coordenada Y")