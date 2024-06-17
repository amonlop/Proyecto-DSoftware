from .models import cardumen, zona
from django.shortcuts import  render, redirect
from .forms import crearCardumen, ingresarCoordenadas
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def database(request):
    cardumenes = cardumen.objects.all()
    zonas = zona.objects.all()
    return render(request, 'datos.html', {
        'cardumenes':cardumenes, 'zonas':zonas
    })

def crear_cardumen(request):
    if(request.method == 'GET'):
        return render(request, 'crear_cardumen.html', {
        'cardumenForm' : crearCardumen
        })
    else:
        cardumen.objects.create(nombre = request.POST['nombre'])
        return redirect('base_de_datos')
    
def obtener_viaje(request):
    if(request.method == 'GET'):
        return render(request, 'obtener_viaje.html',{
        'lugarForm' : ingresarCoordenadas
        })
    elif request.method == 'POST':

        request.session['coordenadaX'] = request.POST.get('coordenadaX')
        request.session['coordenadaY'] = request.POST.get('coordenadaY')
        return redirect('estadisticas_viaje')

def estadisticas_viaje(request):
    coordenadaX = int(request.session.get('coordenadaX'))
    coordenadaY = int(request.session.get('coordenadaY'))
    zona = {
        'cord_x': coordenadaX,
        'cord_y': coordenadaY,
        'profundidad': 60,
        'temperatura': 35
    }
    apiData = requests.post('http://localhost:5000/probabilidad_exito', json=zona)
    apiData = apiData.json()
    
    return render(request, 'estadisticas_viaje.html',{
        'coordenadaX' : coordenadaX,
        'coordenadaY' : coordenadaY,
        'profundidad' : apiData['profundidad'],
        'temperatura' : apiData['temperatura'],
        'prob_cardumenes' : apiData['cardumenes'],
        'prob_exito' : apiData['probabilidad_exito']
    })
    