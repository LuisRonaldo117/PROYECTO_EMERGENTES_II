from flask import render_template

def list(clientes):
    return render_template('empleados/clientes/index.html', clientes=clientes)
def list(clientes, busqueda=None):
    return render_template('empleados/clientes/index.html', clientes=clientes, busqueda=busqueda)

def create():
    return render_template('empleados/clientes/create.html')

def edit(cliente):
    return render_template('empleados/clientes/edit.html', cliente=cliente)
