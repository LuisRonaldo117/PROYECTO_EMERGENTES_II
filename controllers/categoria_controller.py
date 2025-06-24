from flask import request, redirect, url_for, Blueprint
from models.categoria_model import Categoria
from views import categoria_view

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@categoria_bp.route("/")
def index():
    categorias = Categoria.get_all()
    return categoria_view.list(categorias)

@categoria_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = Categoria(nombre=nombre)
        categoria.save()
        return redirect(url_for('categoria.index'))
    return categoria_view.create()

@categoria_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    categoria = Categoria.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria.update(nombre)
        return redirect(url_for('categoria.index'))
    return categoria_view.edit(categoria)

@categoria_bp.route("/delete/<int:id>")
def delete(id):
    categoria = Categoria.get_by_id(id)
    categoria.delete()
    return redirect(url_for('categoria.index'))
