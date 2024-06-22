from ApiV2 import db
from ApiV2 import CardumenDB, ZonaDB, ViajeDB, ViajeCardumenDB

def calcular_porcentaje_interseccion(zona1, zona2):
    xmin1 = zona1.x_min, xmax1 = zona1.x_max, ymin1 = zona1.y_min, ymax1 = zona1.y_max
    xmin2 = zona2.x_min, xmax2 = zona2.x_max, ymin2 = zona2.y_min, ymax2 = zona2.y_max

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
        

    def duracion_viaje(self):
        return self.fecha_llegada - self.fecha_salida
    
    @staticmethod
    def obtenerViajes(zona):
        viajes = list()
        viajesDB = db.session.query(ViajeDB).all()
        #Filtrar los viajes que cumplan calcular_porcentaje_interseccion(viaje.zona, zona) > 30
        for viaje in viajesDB:
            cardumenes_pescados = db.session.query(ViajeCardumenDB).filter(ViajeCardumenDB.id_viaje == viaje.id).all()
            cardumenes = list()
            for cardumen in cardumenes_pescados:
                cardumenes.append(cardumen.id_cardumen)
            viajes.append(Viaje(zona, viaje.fecha_salida, viaje.fecha_llegada, cardumenes, viaje.es_viaje_exitoso))
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
        conteo_cardumenes = {cardumen.nombre: 0 for cardumen in self.cardumenes}
        total_viajes = 0

        for viaje in self.viajes_historicos:
            if (viaje.zona.cord_x == zona.cord_x and
                viaje.zona.cord_y == zona.cord_y and
                viaje.zona.profundidad == zona.profundidad and
                viaje.zona.temperatura == zona.temperatura):
                total_viajes += 1
                for cardumen_pescado in viaje.cardumenes_pescados:
                    conteo_cardumenes[cardumen_pescado] += 1

        probabilidades = []
        if total_viajes > 0:
            for cardumen in self.cardumenes:
                probabilidad_aparicion = (conteo_cardumenes[cardumen.nombre] / total_viajes) * 100
                probabilidades.append(probabilidadCardumen(cardumen.nombre, probabilidad_aparicion))
        else:
            for cardumen in self.cardumenes:
                if cardumen.puede_habitar(zona):
                    probabilidades.append(probabilidadCardumen(cardumen.nombre, 100))

        return probabilidades

    def pExito(self, zona):
        viajes_en_zona = [viaje for viaje in self.viajes_historicos if
                          viaje.zona.cord_x == zona.cord_x and
                          viaje.zona.cord_y == zona.cord_y and
                          viaje.zona.profundidad == zona.profundidad and
                          viaje.zona.temperatura == zona.temperatura]

        if not viajes_en_zona:
            return 15.0

        exito_count = sum(viaje.es_exitoso for viaje in viajes_en_zona)
        resultado = (exito_count / len(viajes_en_zona) * 100) + 15
        if resultado > 100:
            resultado = 100
        return resultado

    def posibles_cardumenes(self, zona):
        posibles = [cardumen.nombre for cardumen in self.cardumenes if cardumen.puede_habitar(zona)]
        return posibles

# Ejemplo de uso
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

def main():
    zona_nueva = Zona(cord_x=20, cord_y=55, profundidad=60, temperatura=20)
    calculadora = CalculadoraProbabilistica(cardumenes, viajes_historicos)

    probabilidades_cardumen = calculadora.pCardumen(zona_nueva)
    probabilidad_exito = calculadora.pExito(zona_nueva)

    print("Probabilidades de cardúmenes en la zona nueva basado en datos históricos:")
    if all(probabilidad.probabilidad_aparicion == 0 for probabilidad in probabilidades_cardumen):
        print("No hay datos históricos para esta zona")
        posibles = calculadora.posibles_cardumenes(zona_nueva)
        if posibles:
            print("Pero cumple las condiciones donde habitan los siguientes cardúmenes:")
            for especie in posibles:
                print(especie)
        else:
            print("No hay cardúmenes que habiten en esta zona")

    else:
        for probabilidad in probabilidades_cardumen:
            if probabilidad.probabilidad_aparicion > 0:
                print(f"{probabilidad.especie}: {probabilidad.probabilidad_aparicion:.2f}%")

    print(f"Probabilidad de éxito de viajes anteriores con condiciones similares: {probabilidad_exito:.2f}%")

if __name__ == "__main__":
    main()
