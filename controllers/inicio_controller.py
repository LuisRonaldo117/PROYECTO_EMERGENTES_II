# controllers/inicio_controller.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models.producto_model import Producto
from models.venta_model import Venta
from models.cliente_model import Cliente
from models.empleado_model import Empleado
from database import db
from sqlalchemy import func
from datetime import date

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        flash('Acceso denegado: solo administradores', 'danger')
        return redirect(url_for('inicio.home'))

    hoy = date.today()
    
    total_productos = Producto.query.count()
    productos_bajo_stock = Producto.query.filter(Producto.stock < 30).count()
    ventas_hoy = Venta.query.filter(func.date(Venta.fecha) == hoy).count()
    ganancias_hoy = db.session.query(func.coalesce(func.sum(Venta.total), 0)).filter(func.date(Venta.fecha) == hoy).scalar()
    total_clientes = Cliente.query.count()
    total_empleados = Empleado.query.count()  # Sin filtrar por estado

    return render_template('inicio/panel_inicio.html',
                           total_productos=total_productos,
                           productos_bajo_stock=productos_bajo_stock,
                           ventas_hoy=ventas_hoy,
                           ganancias_hoy=ganancias_hoy,
                           total_clientes=total_clientes,
                           total_empleados=total_empleados)

@inicio_bp.route('/')
def home():
    return redirect(url_for('login'))
