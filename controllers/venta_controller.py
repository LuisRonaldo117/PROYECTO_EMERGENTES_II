from flask import request,redirect,url_for,Blueprint
from datetime import datetime

from models.venta_model import Venta
from models.producto_model import Producto
from models.cliente_model import Cliente

from views import venta_view

venta_bp = Blueprint('venta',__name__,url_prefix='/ventas')

@venta_bp.route("/")
def index():
    # Recupera todos los registros de ventas
    ventas = Venta.get_all()
    return venta_view.list(ventas)

@venta_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']
        fecha_str = request.form['fecha']
        
        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()

        
        venta = Venta(cliente_id=cliente_id,producto_id=producto_id,cantidad=cantidad,fecha=fecha)
        venta.save()
        return redirect(url_for('venta.index'))
    
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    
    return venta_view.create(clientes, productos)

@venta_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    venta = Venta.get_by_id(id)
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']
        fecha_str = request.form['fecha']
        
        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
        #actualizar
        venta.update(cliente_id=cliente_id,producto_id=producto_id,cantidad=cantidad,fecha=fecha)
        return redirect(url_for('venta.index'))
    
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return venta_view.edit(venta,clientes,productos)

@venta_bp.route("/delete/<int:id>")
def delete(id):
    venta = Venta.get_by_id(id)
    venta.delete()
    return redirect(url_for('venta.index'))