from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.venta_model import Venta
from models.cliente_model import Cliente
from models.empleado_model import Empleado
from models.modelo_vehiculo_model import ModeloVehiculo
from models.detalle_venta_model import DetalleVenta
from models.producto_model import Producto
from database import db
from flask_login import login_required
venta_bp = Blueprint('venta', __name__, url_prefix='/ventas')

@venta_bp.route('/')
@login_required
def index():
    ventas = Venta.get_all()
    return render_template('ventas/index.html', ventas=ventas)

@venta_bp.route('/create', methods=['GET', 'POST'])
def create():
    clientes = Cliente.query.all()
    empleados = Empleado.query.all()
    modelos = ModeloVehiculo.get_all()
    productos = Producto.get_all()

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        empleado_id = request.form.get('empleado_id')
        metodo_pago = request.form.get('metodo_pago')
        modelo_vehiculo_id = request.form.get('modelo_vehiculo_id') or None
        total = float(request.form.get('total') or 0)

        # Crear la venta
        venta = Venta(
            cliente_id=cliente_id,
            empleado_id=empleado_id,
            metodo_pago=metodo_pago,
            modelo_vehiculo_id=modelo_vehiculo_id,
            total=total
        )
        venta.save()

        # Aquí puedes procesar detalles (productos, cantidades, precios)
        # Por simplicidad, luego puedes extender este bloque

        flash('Venta creada correctamente.', 'success')
        return redirect(url_for('venta.index'))

    return render_template('ventas/create.html', clientes=clientes, empleados=empleados, modelos=modelos, productos=productos)


# 🧾 NUEVA RUTA: Ver detalle de la venta como factura
@venta_bp.route('/<int:venta_id>/detalle')
def detalle(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    return render_template('ventas/detalle.html', venta=venta)
