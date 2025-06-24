from flask import Blueprint
from models.detalle_venta_model import DetalleVenta

detalle_venta_bp = Blueprint('detalle_venta', __name__, url_prefix='/detalle_venta')

# Aquí funciones según necesidad, pero generalmente es parte de la venta
