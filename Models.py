from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Modelos base de datos
class CardumenDB(db.Model):
    __tablename__ = 'adminBD_cardumen'
    especie = db.Column(db.String(200), primary_key=True)
    profundidad_min = db.Column(db.Integer, nullable=False)
    profundidad_max = db.Column(db.Integer, nullable=False)
    temp_min = db.Column(db.Integer, nullable=False)
    temp_max = db.Column(db.Integer, nullable=False)
    x_min = db.Column(db.Integer, nullable=False)
    x_max = db.Column(db.Integer, nullable=False)
    y_min = db.Column(db.Integer, nullable=False)
    y_max = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Cardumen {self.nombre}>'

class ZonaDB(db.Model):
    __tablename__ = 'adminBD_zona'
    id = db.Column(db.Integer, primary_key=True)
    x_min = db.Column(db.Integer, nullable=False)
    x_max = db.Column(db.Integer, nullable=False)
    y_min = db.Column(db.Integer, nullable=False)
    y_max = db.Column(db.Integer, nullable=False)
    profundidad = db.Column(db.Integer, nullable=False)
    temperatura = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Zona {self.id}>'

class ViajeDB(db.Model):
    __tablename__ = 'adminBD_viaje'
    id = db.Column(db.Integer, primary_key=True)
    zona_id = db.Column(db.Integer, db.ForeignKey('adminBD_zona.id'), nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)
    fecha_llegada = db.Column(db.Date, nullable=False)
    es_viaje_exitoso = db.Column(db.Boolean, nullable=False)
    zona = db.relationship('ZonaDB', backref=db.backref('viajes', lazy=True))

    def __repr__(self):
        return f"<Viaje {self.id}>"

class ViajeCardumenDB(db.Model):
    __tablename__ = 'adminBD_viajecardumen'
    id = db.Column(db.Integer, primary_key=True)
    viaje_id = db.Column(db.Integer, db.ForeignKey('adminBD_viaje.id'), nullable=False)
    cardumen_id = db.Column(db.String(200), db.ForeignKey('adminBD_cardumen.especie'), nullable=False)
    viaje = db.relationship('ViajeDB', backref=db.backref('viaje_cardumen', lazy=True))
    cardumen = db.relationship('CardumenDB', backref=db.backref('viaje_cardumen', lazy=True))

    def __repr__(self):
        return f"<Viaje {self.viaje_id} | Cardumen {self.cardumen_id}>"
