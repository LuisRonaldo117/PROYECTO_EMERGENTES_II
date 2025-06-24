import os
from flask import request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
from database import db

from models.producto_model import Producto, ProductoProveedor
from models.categoria_model import Categoria
from models.proveedor_model import Proveedor
from views import producto_view

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

UPLOAD_FOLDER = "static/img/productos"

@producto_bp.route("/")
def index():
    categoria_id = request.args.get('categoria_id', type=int)
    q = request.args.get('q', '').strip()

    query = Producto.query

    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    if q:
        query = query.filter(Producto.nombre.ilike(f'%{q}%'))

    productos = query.all()
    categorias = Categoria.get_all()

    # Asegúrate que la vista 'list' acepte categorias y los filtros para renderizar el formulario
    return producto_view.list(productos, categorias=categorias, categoria_seleccionada=categoria_id, busqueda=q)

@producto_bp.route("/create", methods=['GET', 'POST'])
def create():
    categorias = Categoria.get_all()
    proveedores = Proveedor.get_all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        categoria_id = int(request.form['categoria_id'])
        proveedor_id = int(request.form['proveedor_id'])
        precio_compra = float(request.form['precio_compra'])

        imagen_file = request.files['imagen']
        imagen_nombre = None

        if imagen_file:
            imagen_nombre = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join(UPLOAD_FOLDER, imagen_nombre))

        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio,
                            stock=stock, imagen=imagen_nombre, categoria_id=categoria_id)
        producto.save()

        registro = ProductoProveedor(
            producto_id=producto.id,
            proveedor_id=proveedor_id,
            cantidad=stock,
            precio_compra=precio_compra,
            total=stock * precio_compra
        )
        db.session.add(registro)
        db.session.commit()

        return redirect(url_for('producto.index'))

    return producto_view.create(categorias, proveedores)

@producto_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    producto = Producto.get_by_id(id)
    categorias = Categoria.get_all()
    proveedores = Proveedor.get_all()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            return redirect(url_for('producto.edit', id=id))

        producto.nombre = nombre
        producto.descripcion = request.form.get('descripcion', '')
        producto.precio = float(request.form.get('precio', 0))
        producto.stock = int(request.form.get('stock', 0))
        producto.categoria_id = int(request.form.get('categoria_id', 0))

        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename != '':
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            imagen_nombre = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join(UPLOAD_FOLDER, imagen_nombre))
            producto.imagen = imagen_nombre

        producto.update()
        return redirect(url_for('producto.index'))

    return producto_view.edit(producto, categorias, proveedores)

@producto_bp.route("/delete/<int:id>")
def delete(id):
    from models.detalle_venta_model import DetalleVenta  # o cambia al nombre correcto

    producto = Producto.get_by_id(id)
    if not producto:
        return redirect(url_for('producto.index'))

    DetalleVenta.query.filter_by(producto_id=id).delete()
    ProductoProveedor.query.filter_by(producto_id=id).delete()
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('producto.index'))

