class Cardumen:
    def __init__(self, nombre, profundidad_min, profundidad_max, temp_min, temp_max, xmin, xmax, ymin, ymax):
        self.nombre = nombre
        self.profundidad_min = profundidad_min
        self.profundidad_max = profundidad_max
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    @staticmethod
    def cargar_cardumenes():
        cardumenes = list()
        cardumenes.append(Cardumen("Jurel", 0, 80, 10, 20, 0, 30, 30, 60))
        cardumenes.append(Cardumen("Corvina", 0, 80, 15, 25, 0, 30, 30, 60))
        cardumenes.append(Cardumen("Merluza", 0, 80, 20, 30, 30, 60, 60, 90))
        cardumenes.append(Cardumen("Congrio", 0, 80, 25, 35, 30, 60, 60, 90))
        cardumenes.append(Cardumen("Salmón", 0, 80, 18, 40, 60, 90, 90, 120))
        cardumenes.append(Cardumen("Reineta", 0, 80, 18, 45, 60, 90, 90, 120))
        return cardumenes

    def puede_habitar(self, zona):
        return (self.profundidad_min <= zona.profundidad <= self.profundidad_max and
                self.temp_min <= zona.temperatura <= self.temp_max and
                self.xmin <= zona.cord_x <= self.xmax and
                self.ymin <= zona.cord_y <= self.ymax)

class probabilidadCardumen:
    def __init__(self, especie, probabilidad_aparicion):
        self.especie = especie
        self.probabilidad_aparicion = probabilidad_aparicion

class Viaje:
    def __init__(self, fecha_salida, fecha_llegada, cord_x, cord_y, profundidad, temperatura, cardumenes_pescados, es_exitoso):
        self.fecha_salida = fecha_salida
        self.fecha_llegada = fecha_llegada
        self.es_exitoso = es_exitoso
        self.zona = Zona(cord_x, cord_y, profundidad, temperatura)
        self.cardumenes_pescados = cardumenes_pescados

    def duracion_viaje(self):
        return self.fecha_llegada - self.fecha_salida

class Zona:
    def __init__(self, cord_x, cord_y, profundidad, temperatura):
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.profundidad = profundidad
        self.temperatura = temperatura

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
                probabilidades.append(probabilidadCardumen(cardumen.nombre, 0.0))

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
