from flask import render_template

def mostrar(carrito):
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render_template('carrito/index.html', carrito=carrito, total=total)
