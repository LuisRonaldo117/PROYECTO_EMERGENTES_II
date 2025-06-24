from database import db

class ModeloVehiculo(db.Model):
    __tablename__ = "modelos_vehiculos"

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)

    ventas = db.relationship("Venta", back_populates="modelo_vehiculo")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ModeloVehiculo.query.all()

    @staticmethod
    def get_by_id(id):
        return ModeloVehiculo.query.get(id)
