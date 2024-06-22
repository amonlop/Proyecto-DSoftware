from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from CalculadoraV2 import Cardumen, Zona, CalculadoraProbabilistica, Viaje

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite: ./Proyecto Empresa pesquera/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelos base de datos
class Cardumen(db.Model):
    __tablename__ = 'cardumen'
    nombre = db.Column(db.String(200), primary_key=True)

    def __repr__(self):
        return f'<Cardumen {self.nombre}>'

class Zona(db.Model):
    __tablename__ = 'zona'
    id = db.Column(db.Integer, primary_key=True)
    coordenadaX = db.Column(db.Integer, nullable=False)
    coordenadaY = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint('coordenadaX', 'coordenadaY', name='zona_key'),)

    def __repr__(self):
        return f'<Zona {self.id}>'


# Carga de datos iniciales
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

calculadora = CalculadoraProbabilistica(cardumenes, viajes_historicos)

@app.route('/probabilidad_exito', methods=['POST'])
def probabilidad_exito():
    data = request.json
    zona = Zona(data['cord_x'], data['cord_y'], data['profundidad'], data['temperatura'])
    cardumen = calculadora.pCardumen(zona)
    probabilidad = calculadora.pExito(zona)

    cardumen_list = [{"especie": c.especie, "probabilidad_aparicion": c.probabilidad_aparicion} for c in cardumen]


    return jsonify({
        'cord_x': zona.cord_x,
        'cord_y': zona.cord_y,
        'profundidad': zona.profundidad,
        'temperatura': zona.temperatura,
        'probabilidad_exito': probabilidad,
        'cardumenes': cardumen_list
    })

if __name__ == '__main__':
    app.run(debug=True)
