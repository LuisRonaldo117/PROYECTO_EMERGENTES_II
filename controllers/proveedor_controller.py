from flask import request, redirect, url_for, Blueprint
from models.proveedor_model import Proveedor
from flask_login import login_required
from views import proveedor_view

proveedor_bp = Blueprint('proveedor', __name__, url_prefix='/proveedores')

@proveedor_bp.route("/")
@login_required
def index():
    proveedores = Proveedor.get_all()
    return proveedor_view.list(proveedores)

@proveedor_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        telefono = request.form['telefono']

        proveedor = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono)
        proveedor.save()
        return redirect(url_for('proveedor.index'))

    return proveedor_view.create()

@proveedor_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    proveedor = Proveedor.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        telefono = request.form['telefono']

        proveedor.update(nombre=nombre, contacto=contacto, telefono=telefono)
        return redirect(url_for('proveedor.index'))

    return proveedor_view.edit(proveedor)

@proveedor_bp.route("/delete/<int:id>")
def delete(id):
    proveedor = Proveedor.get_by_id(id)
    proveedor.delete()
    return redirect(url_for('proveedor.index'))
