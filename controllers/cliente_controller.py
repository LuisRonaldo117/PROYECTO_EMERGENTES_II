from flask import request, redirect, url_for, Blueprint, abort, render_template
from models.cliente_model import Cliente
from flask_login import login_required
cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/')
@login_required
def index():
    clientes = Cliente.get_all()  # Devuelve lista de clientes
    return render_template('clientes/index.html', clientes=clientes)

@cliente_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        cliente = Cliente(nombre, email, telefono)
        cliente.save()
        return redirect(url_for('cliente.index'))

    return render_template('clientes/create.html')

@cliente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cliente = Cliente.get_by_id(id)
    if not cliente:
        abort(404)

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        cliente.update(nombre=nombre, email=email, telefono=telefono)
        return redirect(url_for('cliente.index'))

    return render_template('clientes/edit.html', cliente=cliente)

@cliente_bp.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    cliente = Cliente.get_by_id(id)
    if not cliente:
        abort(404)

    cliente.delete()
    return redirect(url_for('cliente.index'))

@cliente_bp.route('/<int:id>/historial')
def historial(id):
    cliente = Cliente.get_by_id(id)
    if not cliente:
        abort(404)
    # Aquí enviamos el cliente a la vista historial.html para mostrar sus ventas y detalles
    return render_template('clientes/historial.html', cliente=cliente)
