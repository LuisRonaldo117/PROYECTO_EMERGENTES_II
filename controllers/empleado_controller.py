from flask import request, redirect, url_for, Blueprint
from models.empleado_model import Empleado
from models.usuario_model import Usuario
from models.producto_model import Producto  # importar modelo Producto
from models.categoria_model import Categoria  # importar modelo Categoria
from views import empleado_view
from flask_login import login_required  # para proteger la ruta

empleado_bp = Blueprint('empleado', __name__, url_prefix='/empleados')

@empleado_bp.route("/")
@login_required
def index():
    empleados = Empleado.get_all()
    return empleado_view.list(empleados)

@empleado_bp.route("/create", methods=['GET', 'POST'])
def create():
    usuarios = Usuario.get_all()
    if request.method == 'POST':
        nombre = request.form['nombre']
        ci = request.form['ci']
        telefono = request.form['telefono']
        usuario_id = request.form['usuario_id']

        empleado = Empleado(nombre=nombre, ci=ci, telefono=telefono, usuario_id=usuario_id)
        empleado.save()
        return redirect(url_for('empleado.index'))
    return empleado_view.create(usuarios)

@empleado_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    empleado = Empleado.get_by_id(id)
    usuarios = Usuario.get_all()
    if request.method == 'POST':
        nombre = request.form['nombre']
        ci = request.form['ci']
        telefono = request.form['telefono']
        usuario_id = request.form['usuario_id']

        empleado.update(nombre=nombre, ci=ci, telefono=telefono, usuario_id=usuario_id)
        return redirect(url_for('empleado.index'))
    return empleado_view.edit(empleado, usuarios)

@empleado_bp.route("/delete/<int:id>")
def delete(id):
    empleado = Empleado.get_by_id(id)
    empleado.delete()
    return redirect(url_for('empleado.index'))

# Nueva ruta para mostrar productos para empleados
@empleado_bp.route("/productos/", methods=['GET', 'POST'])
@login_required
def productos():
    categorias = Categoria.get_all()
    categoria_seleccionada = request.args.get('categoria_id', type=int)

    if categoria_seleccionada:
        productos = Producto.query.filter_by(categoria_id=categoria_seleccionada).all()
    else:
        productos = Producto.get_all()

    return empleado_view.productos(categorias=categorias, productos=productos, categoria_seleccionada=categoria_seleccionada)
