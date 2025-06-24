from database import db

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    
    productos = db.relationship("Producto", back_populates="categoria")

    # Métodos CRUD
    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Categoria.query.all()

    @staticmethod
    def get_by_id(id):
        return Categoria.query.get(id)

    def update(self, nombre):
        self.nombre = nombre
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
