from flask import Blueprint, render_template, request, redirect, url_for
from models.cliente_model import Cliente
from views import empleado_cliente_view  # vistas específicas para empleados
from flask_login import login_required  # para proteger la ruta
empleado_cliente_bp = Blueprint('empleado_cliente', __name__, url_prefix='/empleados/clientes')

@empleado_cliente_bp.route('/')
@login_required
def index():
    # Obtener el texto buscado del query param 'q'
    busqueda = request.args.get('q', '').strip()

    if busqueda:
        # Filtrar clientes cuyo nombre o email contengan el texto buscado (sin importar mayúsculas/minúsculas)
        clientes = Cliente.query.filter(
            (Cliente.nombre.ilike(f'%{busqueda}%')) | (Cliente.email.ilike(f'%{busqueda}%'))
        ).all()
    else:
        # Si no hay búsqueda, obtener todos los clientes
        clientes = Cliente.get_all()

    # IMPORTANTE: retornar la vista renderizada
    return empleado_cliente_view.list(clientes, busqueda=busqueda)

@empleado_cliente_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        cliente = Cliente(nombre=nombre, email=email, telefono=telefono)
        cliente.save()
        return redirect(url_for('empleado_cliente.index'))
    return empleado_cliente_view.create()

@empleado_cliente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cliente = Cliente.get_by_id(id)
    if not cliente:
        return redirect(url_for('empleado_cliente.index'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        cliente.update(nombre=nombre, email=email, telefono=telefono)
        return redirect(url_for('empleado_cliente.index'))
    
    return empleado_cliente_view.edit(cliente)

@empleado_cliente_bp.route('/delete/<int:id>')
def delete(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        cliente.delete()
    return redirect(url_for('empleado_cliente.index'))
