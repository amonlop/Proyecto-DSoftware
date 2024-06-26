from django import forms

class ingresarCoordenadas(forms.Form):
    coordenadaX1 = forms.IntegerField(label="coordenada X_1")
    coordenadaX2 = forms.IntegerField(label="coordenada X_2")
    coordenadaY1 = forms.IntegerField(label="coordenada Y_1")
    coordenadaY2 = forms.IntegerField(label="coordenada Y_2")
    