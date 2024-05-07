import random
from flask import Flask, jsonify

#Hay que acceder a http://127.0.0.1:5000/api/cardumenes para ver los datos

# Descripcion: Prototipo de API REST para la obtención de datos de cardúmenes de peces
app = Flask(__name__)

#Tipos de peces en cardumenes
PECES = ("Jurel", "Corvina", "Merluza", "Congrio", "Salmón", "Reineta")
random.seed(0)

#Funciones para generar datos aleatorios
def generarCoordenada(min, max):
    random_float = -1 * random.uniform(min, max)
    formatted_float = "{:0.5f}".format(random_float)
    return  formatted_float
def generarLatitud():
    return generarCoordenada(35, 37)
def generarLongitud():
    return generarCoordenada(72,74)
def generarPescado():
    return PECES[random.randint(0, 5)]

def generarCardumen(id):
    cardumen = {"id = ": id, "especie": generarPescado(), "latitud": generarLatitud(), "longitud": generarLongitud(), "temperatura(Celsius)": random.randint(10, 20), "profundidad(Metros)": random.randint(10, 100)}
    return cardumen

cardumenes = list()
index = 0
for i in range(10):
    cardumenes.append(generarCardumen(index))
    index += 1

@app.route('/api/cardumenes', methods=['GET'])
def get_cardumenes():
    return jsonify(cardumenes)

@app.route('/api/cardumenes/<int:id>', methods=['GET'])
def get_cardumen(id):
    return jsonify(cardumenes[id])

if __name__ == '__main__':
    app.run(debug = True)