from flask import render_template

def list(productos, categorias=None, categoria_seleccionada=None, busqueda=None):
    return render_template(
        "productos/index.html",
        productos=productos,
        categorias=categorias,
        categoria_seleccionada=categoria_seleccionada,
        busqueda=busqueda
    )

def create(categorias, proveedores):
    return render_template("productos/create.html", categorias=categorias, proveedores=proveedores)

def edit(producto, categorias, proveedores):
    return render_template("productos/edit.html", producto=producto, categorias=categorias, proveedores=proveedores)
