from database import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"))

    # Relaciones
    categoria = db.relationship("Categoria", back_populates="productos")
    proveedores = db.relationship("ProductoProveedor", back_populates="producto")
    detalles_venta = db.relationship("DetalleVenta", back_populates="producto")


    # Métodos CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(int(id))


class ProductoProveedor(db.Model):
    __tablename__ = "producto_proveedor"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"))
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedores.id"))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_compra = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, nullable=False)

    producto = db.relationship("Producto", back_populates="proveedores")
    proveedor = db.relationship("Proveedor", back_populates="productos")  # Asegúrate de tener esto también en el modelo `Proveedor`
