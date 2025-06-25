from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from flask_login import current_user
from datetime import datetime

from database import db
from models.producto_model import Producto
from models.venta_model import Venta
from models.detalle_venta_model import DetalleVenta
from models.cliente_model import Cliente
from models.modelo_vehiculo_model import ModeloVehiculo

carrito_empleado_bp = Blueprint('carrito_empleado', __name__, url_prefix='/empleados/carrito')

# Agregar producto al carrito
@carrito_empleado_bp.route('/agregar', methods=['POST'])
def agregar():
    producto_id = request.form.get('producto_id')
    if not producto_id:
        flash("Producto no válido", "danger")
        return redirect(url_for('empleado.productos'))

    producto = Producto.get_by_id(producto_id)
    if not producto:
        flash("Producto no encontrado", "warning")
        return redirect(url_for('empleado.productos'))

    if 'carrito' not in session:
        session['carrito'] = {}

    carrito = session['carrito']

    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
    else:
        carrito[producto_id] = {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1,
            'imagen': producto.imagen
        }

    session['carrito'] = carrito
    flash(f"{producto.nombre} añadido al carrito", "success")
    return redirect(url_for('empleado.productos'))

# Mostrar el carrito
@carrito_empleado_bp.route('/')
def mostrar_carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    modelos_vehiculos = ModeloVehiculo.query.all()
    clientes = Cliente.query.all()
    return render_template(
        'empleados/carrito/index.html',
        carrito=carrito,
        total=total,
        modelos_vehiculos=modelos_vehiculos,
        clientes=clientes
    )

# Vaciar carrito
@carrito_empleado_bp.route('/vaciar', methods=['POST'])
def vaciar_carrito():
    session.pop('carrito', None)
    flash("El carrito ha sido vaciado", "info")
    return redirect(url_for('carrito_empleado.mostrar_carrito'))

# Incrementar cantidad
@carrito_empleado_bp.route('/incrementar/<producto_id>', methods=['POST'])
def incrementar(producto_id):
    carrito = session.get('carrito', {})
    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
    session['carrito'] = carrito
    return redirect(url_for('carrito_empleado.mostrar_carrito'))

# Disminuir cantidad
@carrito_empleado_bp.route('/disminuir/<producto_id>', methods=['POST'])
def disminuir(producto_id):
    carrito = session.get('carrito', {})
    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] > 1:
            carrito[producto_id]['cantidad'] -= 1
        else:
            carrito.pop(producto_id)
    session['carrito'] = carrito
    return redirect(url_for('carrito_empleado.mostrar_carrito'))

# Confirmar compra → crear venta + detalle + redirigir a factura
@carrito_empleado_bp.route('/confirmar', methods=['POST'])
def confirmar_compra():
    carrito = session.get('carrito', {})
    if not carrito:
        flash("El carrito está vacío", "warning")
        return redirect(url_for('carrito_empleado.mostrar_carrito'))

    cliente_id = request.form.get('cliente_id')
    metodo_pago = request.form.get('metodo_pago')
    modelo_vehiculo_id = request.form.get('modelo_vehiculo_id') or None

    if not cliente_id or not metodo_pago:
        flash("Debe seleccionar cliente y método de pago", "danger")
        return redirect(url_for('carrito_empleado.mostrar_carrito'))

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash("Cliente no válido", "danger")
        return redirect(url_for('carrito_empleado.mostrar_carrito'))

    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    empleado = current_user.empleado

    venta = Venta(
        fecha=datetime.utcnow(),
        cliente_id=cliente.id,
        empleado_id=empleado.id,
        metodo_pago=metodo_pago,
        modelo_vehiculo_id=modelo_vehiculo_id,
        total=total
    )

    db.session.add(venta)
    db.session.flush()  # Obtener venta.id antes del commit

    for producto_id, item in carrito.items():
        detalle = DetalleVenta(
            venta_id=venta.id,
            producto_id=int(producto_id),
            cantidad=item['cantidad'],
            precio_unitario=item['precio'],
            subtotal=item['precio'] * item['cantidad']
        )
        db.session.add(detalle)

        producto = Producto.get_by_id(producto_id)
        if producto:
            producto.stock -= item['cantidad']
            if producto.stock < 0:
                producto.stock = 0

    db.session.commit()
    session.pop('carrito', None)

    flash("Compra confirmada exitosamente", "success")
    return redirect(url_for('carrito_empleado.factura', venta_id=venta.id))

# Mostrar factura tras confirmar compra
@carrito_empleado_bp.route('/factura/<int:venta_id>')
def factura(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    return render_template('empleados/carrito/factura.html', venta=venta)
