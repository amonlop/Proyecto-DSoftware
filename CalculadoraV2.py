from Models import db, CardumenDB, ViajeDB, ViajeCardumenDB
import math

def calcular_porcentaje_interseccion(zona1, zona2):
    xmin1 = zona1.x_min
    xmax1 = zona1.x_max
    ymin1 = zona1.y_min
    ymax1 = zona1.y_max
    xmin2 = zona2.x_min
    xmax2 = zona2.x_max
    ymin2 = zona2.y_min
    ymax2 = zona2.y_max

    interseccion_xmin = max(xmin1, xmin2)
    interseccion_xmax = min(xmax1, xmax2)
    interseccion_ymin = max(ymin1, ymin2)
    interseccion_ymax = min(ymax1, ymax2)

    if interseccion_xmax < interseccion_xmin or interseccion_ymax < interseccion_ymin:
        return 0

    área_zona1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    área_intersección = (interseccion_xmax - interseccion_xmin) * (interseccion_ymax - interseccion_ymin)

    porcentaje = (área_intersección / área_zona1) * 100
    return porcentaje

def truncar(numero):
    factor = 10 ** 2
    return math.trunc(numero * factor) / factor

class Zona:
    def __init__(self, x_min, x_max, y_min, y_max, profundidad, temperatura):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.profundidad = profundidad
        self.temperatura = temperatura
    

class Cardumen:
    def __init__(self, especie, profundidad_min, profundidad_max, temp_min, temp_max, x_min, x_max, y_min, y_max):
        self.especie = especie
        self.profundidad_min = profundidad_min
        self.profundidad_max = profundidad_max
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    @staticmethod
    def obtenerCardumenes():
        cardumenes = list()
        cardumenesDB = db.session.query(CardumenDB).all()
        for cardumen in cardumenesDB:
            cardumenes.append(Cardumen(cardumen.especie, cardumen.profundidad_min, cardumen.profundidad_max, cardumen.temp_min, cardumen.temp_max, cardumen.x_min, cardumen.x_max, cardumen.y_min, cardumen.y_max))
        return cardumenes

    def puede_habitar(self, zona):
        return (self.profundidad_min <= zona.profundidad <= self.profundidad_max and
                self.temp_min <= zona.temperatura <= self.temp_max and
                ((self.x_min <= zona.x_min <= self.x_max and
                self.y_min <= zona.y_min <= self.y_max) or (self.x_min <= zona.x_min <= self.x_max and
                self.y_min <= zona.y_max <= self.y_max) or (self.x_min <= zona.x_max <= self.x_max and
                self.y_min <= zona.y_min <= self.y_max) or (self.x_min <= zona.x_max <= self.x_max and
                self.y_min <= zona.y_max <= self.y_max)))
    
class Viaje:
    def __init__(self, zona, fecha_salida, fecha_llegada, cardumenes_pescados, es_exitoso):
        self.zona = zona
        self.fecha_salida = fecha_salida
        self.fecha_llegada = fecha_llegada
        self.es_exitoso = es_exitoso
        self.cardumenes_pescados = cardumenes_pescados
    
    @staticmethod
    def obtenerViajes():
        viajes = list()
        viajesDB = db.session.query(ViajeDB).all()
        
        for viaje in viajesDB:
            cardumenes_pescados = db.session.query(ViajeCardumenDB).filter(ViajeCardumenDB.viaje_id == viaje.id).all()
            cardumenes = list()
            for cardumen_pescado in cardumenes_pescados:
                cardumen = db.session.query(CardumenDB).filter(CardumenDB.especie == cardumen_pescado.cardumen_id).first()
                cardumenes.append(Cardumen(cardumen.especie, cardumen.profundidad_min, cardumen.profundidad_max, cardumen.temp_min, cardumen.temp_max, cardumen.x_min, cardumen.x_max, cardumen.y_min, cardumen.y_max))
            tmp_viaje = Viaje(viaje.zona, viaje.fecha_salida, viaje.fecha_llegada, cardumenes, viaje.es_viaje_exitoso)
            viajes.append(tmp_viaje)

        return viajes

class probabilidadCardumen:
    def __init__(self, especie, probabilidad_aparicion):
        self.especie = especie
        self.probabilidad_aparicion = probabilidad_aparicion


class CalculadoraProbabilistica:
    def __init__(self, cardumenes, viajes_historicos):
        self.cardumenes = cardumenes
        self.viajes_historicos = viajes_historicos

    def pCardumen(self, zona):
        conteo_cardumenes = {cardumen.especie: 0 for cardumen in self.cardumenes}
        total_viajes = 0

        for viaje in self.viajes_historicos:
            if (calcular_porcentaje_interseccion(viaje.zona, zona) > 40 and
                (-10 <= (viaje.zona.profundidad - zona.profundidad) <= 10) and
                (-7 <= (viaje.zona.temperatura - zona.temperatura) <= 7)):
                total_viajes += 1
                for cardumen_pescado in viaje.cardumenes_pescados:
                    conteo_cardumenes[cardumen_pescado.especie] += 1

        probabilidades = list()
        
        for cardumen in self.cardumenes:
            if cardumen.puede_habitar(zona):
                if((cardumen.profundidad_min <= zona.profundidad <= cardumen.profundidad_max) and
                    (cardumen.temp_min <= zona.temperatura <= cardumen.temp_max)):
                    probabilidad_aparicion = calcular_porcentaje_interseccion(zona, cardumen)
                else:
                    probabilidad_aparicion = 0
                if(probabilidad_aparicion > 0):
                    if(total_viajes > 0):
                        probabilidad_aparicion *= ((conteo_cardumenes[cardumen.especie] / total_viajes) + 0.5)
                    else:
                        probabilidad_aparicion*=0.75
                    if probabilidad_aparicion > 100:
                        probabilidad_aparicion = 100

                if probabilidad_aparicion > 0:
                    probabilidades.append(probabilidadCardumen(cardumen.especie, truncar(probabilidad_aparicion)))

        return probabilidades

    def pExitoZona(self, zona):
        probabilidades_cardumenes = self.pCardumen(zona)
        viajes_en_zona = [viaje for viaje in self.viajes_historicos if
                          calcular_porcentaje_interseccion(viaje.zona, zona) > 40 and
                          -10 < (viaje.zona.profundidad - zona.profundidad) < 10 and
                          -7 < (viaje.zona.temperatura - zona.temperatura) < 7]

        probabilidad_total = 0
        cantidad_cardumenes = len(probabilidades_cardumenes)
        for probabilidad in probabilidades_cardumenes:
            probabilidad_total += probabilidad.probabilidad_aparicion
        
        if(cantidad_cardumenes > 0):
            probabilidad_total = (probabilidad_total / cantidad_cardumenes)*0.75

        if not viajes_en_zona:
            probabilidad_total = truncar(probabilidad_total)
            return probabilidad_total

        exito_count = sum(viaje.es_exitoso for viaje in viajes_en_zona)
        probabilidad_total = probabilidad_total * ((exito_count + exito_count/2) / len(viajes_en_zona))
        if probabilidad_total > 100:
            probabilidad_total = 100

        probabilidad_total = truncar(probabilidad_total)
        return probabilidad_total