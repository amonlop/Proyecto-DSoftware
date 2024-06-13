from django.http import HttpResponse, JsonResponse
from .models import cardumen, zona
from django.shortcuts import  render, redirect
from .forms import crearCardumen, ingresarCoordenadas

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
    coordenadaX = request.session.get('coordenadaX')
    coordenadaY = request.session.get('coordenadaY')
    return render(request, 'estadisticas_viaje.html',{
        'coordenadaX' : coordenadaX,
        'coordenadaY' : coordenadaY
    })
    