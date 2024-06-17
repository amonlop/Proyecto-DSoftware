from django.http import HttpResponse, JsonResponse
from .models import cardumen, zona
from django.shortcuts import  render, redirect
from .forms import crearCardumen, ingresarCoordenadas
from .CalculadoraV2 import Cardumen, probabilidadCardumen, Viaje, Zona, CalculadoraProbabilistica

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
    cardumenes = Cardumen.cargar_cardumenes()
    viajes_historicos = [
        Viaje(fecha_salida="2024-01-01", fecha_llegada="2024-01-02", cord_x=36, cord_y=73, profundidad=5, temperatura=15, cardumenes_pescados=["Jurel"], es_exitoso=True),
        Viaje(fecha_salida="2024-01-02", fecha_llegada="2024-01-03", cord_x=38, cord_y=75, profundidad=10, temperatura=16, cardumenes_pescados=["Corvina"], es_exitoso=True),
        Viaje(fecha_salida="2024-01-03", fecha_llegada="2024-01-04", cord_x=40, cord_y=77, profundidad=20, temperatura=17, cardumenes_pescados=["Merluza"], es_exitoso=False),
        Viaje(fecha_salida="2024-01-04", fecha_llegada="2024-01-05", cord_x=42, cord_y=79, profundidad=15, temperatura=18, cardumenes_pescados=["Congrio"], es_exitoso=True),
        Viaje(fecha_salida="2024-01-05", fecha_llegada="2024-01-06", cord_x=44, cord_y=81, profundidad=13, temperatura=19, cardumenes_pescados=["Salmón"], es_exitoso=True),
        Viaje(fecha_salida="2024-01-06", fecha_llegada="2024-01-07", cord_x=46, cord_y=83, profundidad=17, temperatura=20, cardumenes_pescados=["Reineta"], es_exitoso=True),
        Viaje(fecha_salida="2024-02-01", fecha_llegada="2024-02-02", cord_x=37, cord_y=74, profundidad=30, temperatura=15, cardumenes_pescados=["Jurel"], es_exitoso=True),
        Viaje(fecha_salida="2024-02-02", fecha_llegada="2024-02-03", cord_x=39, cord_y=76, profundidad=80, temperatura=16, cardumenes_pescados=["Corvina"], es_exitoso=True),
        Viaje(fecha_salida="2024-02-03", fecha_llegada="2024-02-04", cord_x=41, cord_y=78, profundidad=52, temperatura=17, cardumenes_pescados=["Merluza"], es_exitoso=False),
        Viaje(fecha_salida="2024-02-04", fecha_llegada="2024-02-05", cord_x=43, cord_y=80, profundidad=58, temperatura=18, cardumenes_pescados=["Congrio"], es_exitoso=True),
        Viaje(fecha_salida="2024-02-05", fecha_llegada="2024-02-06", cord_x=45, cord_y=82, profundidad=60, temperatura=19, cardumenes_pescados=["Salmón"], es_exitoso=False),
        Viaje(fecha_salida="2024-02-06", fecha_llegada="2024-02-07", cord_x=47, cord_y=84, profundidad=62, temperatura=20, cardumenes_pescados=["Reineta"], es_exitoso=True),
        Viaje(fecha_salida="2024-03-01", fecha_llegada="2024-03-02", cord_x=36, cord_y=75, profundidad=50, temperatura=15, cardumenes_pescados=["Jurel"], es_exitoso=True),
        Viaje(fecha_salida="2024-03-02", fecha_llegada="2024-03-03", cord_x=38, cord_y=77, profundidad=52, temperatura=16, cardumenes_pescados=["Corvina"], es_exitoso=True),
        Viaje(fecha_salida="2024-03-03", fecha_llegada="2024-03-04", cord_x=40, cord_y=79, profundidad=55, temperatura=17, cardumenes_pescados=["Merluza"], es_exitoso=False),
        Viaje(fecha_salida="2024-03-04", fecha_llegada="2024-03-05", cord_x=42, cord_y=81, profundidad=58, temperatura=18, cardumenes_pescados=["Congrio"], es_exitoso=True),
        Viaje(fecha_salida="2024-03-05", fecha_llegada="2024-03-06", cord_x=44, cord_y=83, profundidad=60, temperatura=19, cardumenes_pescados=["Salmón"], es_exitoso=False),
        Viaje(fecha_salida="2024-03-06", fecha_llegada="2024-03-07", cord_x=46, cord_y=85, profundidad=62, temperatura=20, cardumenes_pescados=["Reineta"], es_exitoso=True),
        Viaje(fecha_salida="2024-04-01", fecha_llegada="2024-04-02", cord_x=37, cord_y=76, profundidad=50, temperatura=15, cardumenes_pescados=["Jurel"], es_exitoso=True),
        Viaje(fecha_salida="2024-04-02", fecha_llegada="2024-04-03", cord_x=39, cord_y=78, profundidad=52, temperatura=16, cardumenes_pescados=["Corvina"], es_exitoso=True),
        Viaje(fecha_salida="2024-04-03", fecha_llegada="2024-04-04", cord_x=41, cord_y=80, profundidad=55, temperatura=17, cardumenes_pescados=["Merluza"], es_exitoso=False),
        Viaje(fecha_salida="2024-04-04", fecha_llegada="2024-04-05", cord_x=43, cord_y=82, profundidad=58, temperatura=18, cardumenes_pescados=["Congrio"], es_exitoso=True),
        Viaje(fecha_salida="2024-04-05", fecha_llegada="2024-04-06", cord_x=45, cord_y=84, profundidad=60, temperatura=19, cardumenes_pescados=["Salmón"], es_exitoso=False),
    ]
    coordenadaX = request.session.get('coordenadaX')
    coordenadaY = request.session.get('coordenadaY')
    zona_nueva = Zona(cord_x=coordenadaX, cord_y=coordenadaY, profundidad=60, temperatura=20)
    profundidad = zona_nueva.profundidad
    temperatura = zona_nueva.temperatura
    calculadora = CalculadoraProbabilistica(cardumenes, viajes_historicos)
    probabilidades_cardumen = calculadora.pCardumen(zona_nueva)
    return render(request, 'estadisticas_viaje.html',{
        'coordenadaX' : coordenadaX,
        'coordenadaY' : coordenadaY,
        'profundidad' : profundidad,
        'temperatura' : temperatura,
        'probabilidades' : probabilidadCardumen
    })
    