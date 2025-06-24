from database import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    empleado_id = db.Column(db.Integer, db.ForeignKey("empleados.id"))
    metodo_pago = db.Column(db.String(50), nullable=False)
    modelo_vehiculo_id = db.Column(db.Integer, db.ForeignKey("modelos_vehiculos.id"), nullable=True)
    total = db.Column(db.Float, nullable=False)

    cliente = db.relationship("Cliente", back_populates="ventas")
    empleado = db.relationship("Empleado", back_populates="ventas")
    detalles = db.relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    modelo_vehiculo = db.relationship("ModeloVehiculo", back_populates="ventas")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Venta.query.all()

    @staticmethod
    def get_by_id(id):
        return Venta.query.get(id)
