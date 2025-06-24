from database import db

class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    ci = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    usuario = db.relationship("Usuario", back_populates="empleado")
    ventas = db.relationship("Venta", back_populates="empleado")

    def __init__(self, nombre, ci, telefono, usuario_id):
        self.nombre = nombre
        self.ci = ci
        self.telefono = telefono
        self.usuario_id = usuario_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre=None, ci=None, telefono=None, usuario_id=None):
        if nombre:
            self.nombre = nombre
        if ci:
            self.ci = ci
        if telefono:
            self.telefono = telefono
        if usuario_id:
            self.usuario_id = usuario_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Empleado.query.all()

    @staticmethod
    def get_by_id(id):
        return Empleado.query.get(id)

    @staticmethod
    def get_by_usuario_id(usuario_id):
        return Empleado.query.filter_by(usuario_id=usuario_id).first()
