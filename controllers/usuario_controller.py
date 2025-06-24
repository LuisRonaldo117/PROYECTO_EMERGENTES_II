from flask import request, redirect, url_for, Blueprint
from flask_login import login_required
from models.usuario_model import Usuario
from models.empleado_model import Empleado
from views import usuario_view

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route("/")
@login_required
def index():
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Datos del usuario
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']

        # Crear usuario
        usuario = Usuario(username=username, password=password, rol=rol)
        usuario.save()

        # Datos del empleado (siempre se guardan)
        nombre = request.form['nombre']
        ci = request.form['ci']
        telefono = request.form['telefono']

        empleado = Empleado(nombre=nombre, ci=ci, telefono=telefono, usuario_id=usuario.id)
        empleado.save()

        return redirect(url_for('usuario.index'))

    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    usuario = Usuario.get_by_id(id)
    empleado = Empleado.get_by_usuario_id(id)

    if request.method == 'POST':
        # Actualizar usuario
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        usuario.update(username=username, password=password, rol=rol)

        # Actualizar empleado
        nombre = request.form['nombre']
        ci = request.form['ci']
        telefono = request.form['telefono']

        if empleado:
            empleado.update(nombre=nombre, ci=ci, telefono=telefono, usuario_id=usuario.id)

        return redirect(url_for('usuario.index'))

    return usuario_view.edit(usuario, empleado)

@usuario_bp.route("/delete/<int:id>")
def delete(id):
    usuario = Usuario.get_by_id(id)
    empleado = Empleado.get_by_usuario_id(id)

    # Eliminar empleado primero por si hay dependencias
    if empleado:
        empleado.delete()

    # Luego eliminar usuario
    usuario.delete()
    return redirect(url_for('usuario.index'))
