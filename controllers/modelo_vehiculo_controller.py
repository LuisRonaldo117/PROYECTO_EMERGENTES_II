from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.modelo_vehiculo_model import ModeloVehiculo
from flask_login import login_required
modelo_vehiculo_bp = Blueprint('modelo_vehiculo', __name__, url_prefix='/modelos_vehiculos')

@modelo_vehiculo_bp.route('/')
@login_required
def index():
    modelos = ModeloVehiculo.get_all()
    return render_template('modelos_vehiculos/index.html', modelos=modelos)

@modelo_vehiculo_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        anio = request.form.get('anio')

        nuevo_modelo = ModeloVehiculo(marca=marca, modelo=modelo, anio=anio)
        nuevo_modelo.save()
        flash('Modelo de vehículo creado.', 'success')
        return redirect(url_for('modelo_vehiculo.index'))

    return render_template('modelos_vehiculos/create.html')

@modelo_vehiculo_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    modelo_vehiculo = ModeloVehiculo.get_by_id(id)
    if not modelo_vehiculo:
        flash('Modelo no encontrado.', 'error')
        return redirect(url_for('modelo_vehiculo.index'))

    if request.method == 'POST':
        modelo_vehiculo.marca = request.form.get('marca')
        modelo_vehiculo.modelo = request.form.get('modelo')
        modelo_vehiculo.anio = request.form.get('anio')

        modelo_vehiculo.save()
        flash('Modelo actualizado correctamente.', 'success')
        return redirect(url_for('modelo_vehiculo.index'))

    return render_template('modelos_vehiculos/edit.html', modelo=modelo_vehiculo)

# Delete simple vía GET
@modelo_vehiculo_bp.route('/delete/<int:id>')
def delete(id):
    modelo_vehiculo = ModeloVehiculo.query.get_or_404(id)
    modelo_vehiculo.delete()
    flash('Modelo de vehículo eliminado.', 'success')
    return redirect(url_for('modelo_vehiculo.index'))


