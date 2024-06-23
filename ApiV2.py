from flask import Flask, jsonify, request
from CalculadoraV2 import Cardumen, Zona, CalculadoraProbabilistica, Viaje
from Models import db
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'Proyecto Empresa pesquera', 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path.replace('\\', '/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/probabilidad_exito_zona', methods=['POST'])
def probabilidad_exito_zona():
    cardumenes = Cardumen.obtenerCardumenes()
    viajes_historicos = Viaje.obtenerViajes()
    calculadora = CalculadoraProbabilistica(cardumenes, viajes_historicos)

    data = request.json
    zona = Zona(data['x_min'], data['x_max'], data['y_min'], data['y_max'], data['profundidad'], data['temperatura'])
    cardumen = calculadora.pCardumen(zona)
    probabilidad_exito = calculadora.pExitoZona(zona)

    probabilidad_cardumenes = [{"especie": c.especie, "probabilidad_aparicion": c.probabilidad_aparicion} for c in cardumen]


    return jsonify({
        'x_min': zona.x_min,
        'x_max': zona.x_max,
        'y_min': zona.y_min,
        'y_max': zona.y_max,
        'profundidad': zona.profundidad,
        'temperatura': zona.temperatura,
        'probabilidad_exito': probabilidad_exito,
        'probabilidad_cardumenes': probabilidad_cardumenes
    })

if __name__ == '__main__':
    app.run(debug=True)
