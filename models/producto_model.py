from database import db

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float(11,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    
    # relacion con ventas
    ventas = db.relationship('Venta',back_populates='producto')

    def __init__(self, descripcion, precio, stock):
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Producto.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)
    
    def update(self,descripcion=None,precio=None,stock=None):
        if descripcion and precio and stock:
            self.descripcion = descripcion
            self.precio = precio
            self.stock = stock
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    