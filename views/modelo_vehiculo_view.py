from flask import render_template

def list(modelos):
    return render_template('modelos_vehiculos/index.html', modelos=modelos)

def create():
    return render_template('modelos_vehiculos/create.html')

def edit(modelo):
    return render_template('modelos_vehiculos/edit.html', modelo=modelo)
