from django.shortcuts import  render, redirect
from .forms import ingresarCoordenadas
import requests

# Create your views here.
def index(request):
    apiData = requests.get('http://localhost:5000/obtener_viajes')
    apiData = apiData.json()
  
    return render(request, 'index.html', {
        'viajes' : apiData
    })
    
def obtener_viaje(request):
    if(request.method == 'GET'):
        return render(request, 'obtener_viaje.html',{
        'lugarForm' : ingresarCoordenadas
        })
    elif request.method == 'POST':

        request.session['coordenadaX1'] = request.POST.get('coordenadaX1')
        request.session['coordenadaX2'] = request.POST.get('coordenadaX2')
        request.session['coordenadaY1'] = request.POST.get('coordenadaY1')
        request.session['coordenadaY2'] = request.POST.get('coordenadaY2')
        return redirect('estadisticas_viaje')

def estadisticas_viaje(request):
    coordenadaX1 = int(request.session.get('coordenadaX1'))
    coordenadaX2 = int(request.session.get('coordenadaX2'))
    coordenadaY1 = int(request.session.get('coordenadaY1'))
    coordenadaY2 = int(request.session.get('coordenadaY2'))
    zona = {
        'x_min': coordenadaX1,
        'x_max': coordenadaX2,
        'y_min': coordenadaY1,
        'y_max': coordenadaY2,
        'profundidad': 10,
        'temperatura': 15
    }
    apiData = requests.post('http://localhost:5000/probabilidad_exito_zona', json=zona)
    apiData = apiData.json()
    
    return render(request, 'estadisticas_viaje.html',{
        'x_min' : coordenadaX1,
        'x_max' : coordenadaX2,
        'y_min' : coordenadaY1,
        'y_max' : coordenadaY2,
        'profundidad' : apiData['profundidad'],
        'temperatura' : apiData['temperatura'],
        'prob_cardumenes' : apiData['probabilidad_cardumenes'],
        'prob_exito' : apiData['probabilidad_exito']
    })
    