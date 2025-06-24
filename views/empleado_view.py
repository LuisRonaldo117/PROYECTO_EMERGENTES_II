from flask import render_template

def list(empleados):
    return render_template('empleados/index.html', empleados=empleados)

def create(usuarios):
    return render_template('empleados/create.html', usuarios=usuarios)

def edit(empleado, usuarios):
    return render_template('empleados/edit.html', empleado=empleado, usuarios=usuarios)

def productos(categorias, productos, categoria_seleccionada):
    return render_template('empleados/productos.html', 
                           categorias=categorias, 
                           productos=productos, 
                           categoria_seleccionada=categoria_seleccionada)
