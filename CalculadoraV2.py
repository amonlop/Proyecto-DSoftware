from Models import db, CardumenDB, ViajeDB, ViajeCardumenDB

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
    def obtenerViajes():
        viajes = list()
        viajesDB = db.session.query(ViajeDB).all()
        
        for viaje in viajesDB:
            cardumenes_pescados = db.session.query(ViajeCardumenDB).filter(ViajeCardumenDB.id_viaje == viaje.id).all()
            cardumenes = list()
            for cardumen_pescado in cardumenes_pescados:
                cardumen = db.session.query(CardumenDB).filter(CardumenDB.especie == cardumen_pescado.especie_cardumen).first()
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
                (-7 <= (viaje.zona.profundidad - zona.profundidad) <= 7) and
                (-7 <= (viaje.zona.temperatura - zona.temperatura) <= 7)):
                total_viajes += 1
                for cardumen_pescado in viaje.cardumenes_pescados:
                    conteo_cardumenes[cardumen_pescado] += 1

        probabilidades = list()
        
        for cardumen in self.cardumenes:
            if cardumen.puede_habitar(zona):
                if((cardumen.profundidad_min <= zona.profundidad <= cardumen.profundidad_max) and
                    (cardumen.temp_min <= zona.temperatura <= cardumen.temp_max)):
                    probabilidad_aparicion = calcular_porcentaje_interseccion(zona, cardumen)
                else:
                    probabilidad_aparicion = 0
                if(probabilidad_aparicion > 0):
                    probabilidad_aparicion *= ((conteo_cardumenes[cardumen.especie] / total_viajes) + 0.5)
                    if probabilidad_aparicion > 100:
                        probabilidad_aparicion = 100

                probabilidades.append(probabilidadCardumen(cardumen.especie, probabilidad_aparicion))

        return probabilidades

    def pExitoZona(self, zona):
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
    
    def viajeRecomendado(self):
        #inserte algoritmo
        return

    def posibles_cardumenes(self, zona):
        posibles = [cardumen.especie for cardumen in self.cardumenes if cardumen.puede_habitar(zona)]
        return posibles

# Ejemplo de uso
# cardumenes = Cardumen.cargar_cardumenes()
# viajes_historicos = Viaje.cargar_viajes()

# def main():
#     zona_nueva = Zona(cord_x=20, cord_y=55, profundidad=60, temperatura=20)
#     calculadora = CalculadoraProbabilistica(cardumenes, viajes_historicos)

#     probabilidades_cardumen = calculadora.pCardumen(zona_nueva)
#     probabilidad_exito = calculadora.pExito(zona_nueva)

#     print("Probabilidades de cardúmenes en la zona nueva basado en datos históricos:")
#     if all(probabilidad.probabilidad_aparicion == 0 for probabilidad in probabilidades_cardumen):
#         print("No hay datos históricos para esta zona")
#         posibles = calculadora.posibles_cardumenes(zona_nueva)
#         if posibles:
#             print("Pero cumple las condiciones donde habitan los siguientes cardúmenes:")
#             for especie in posibles:
#                 print(especie)
#         else:
#             print("No hay cardúmenes que habiten en esta zona")

#     else:
#         for probabilidad in probabilidades_cardumen:
#             if probabilidad.probabilidad_aparicion > 0:
#                 print(f"{probabilidad.especie}: {probabilidad.probabilidad_aparicion:.2f}%")

#     print(f"Probabilidad de éxito de viajes anteriores con condiciones similares: {probabilidad_exito:.2f}%")

# if __name__ == "__main__":
#     main()
