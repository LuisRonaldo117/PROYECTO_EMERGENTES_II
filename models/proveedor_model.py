from database import db

class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    
    productos = db.relationship("ProductoProveedor", back_populates="proveedor")

    def __init__(self, nombre, contacto, telefono):
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Proveedor.query.all()

    @staticmethod
    def get_by_id(id):
        return Proveedor.query.get(id)

    def update(self, nombre=None, contacto=None, telefono=None):
        if nombre:
            self.nombre = nombre
        if contacto:
            self.contacto = contacto
        if telefono:
            self.telefono = telefono
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
