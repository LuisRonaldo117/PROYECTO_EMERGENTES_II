from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from controllers import usuario_controller, cliente_controller, producto_controller, venta_controller, empleado_controller,proveedor_controller
from controllers import categoria_controller, empleado_cliente_controller, carrito_empleado_controller
from controllers import detalle_venta_controller, modelo_vehiculo_controller
from models.usuario_model import Usuario  # Tu modelo Usuario debe implementar UserMixin
from database import db

#from sqlalchemy import text
app = Flask(__name__)
app.secret_key = 'clave-secreta-123'  # Necesaria para sesiones y seguridad

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # Ruta a donde redirige si no está logueado
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))  # Devuelve usuario por id o None

# Registrar blueprints
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)
app.register_blueprint(empleado_controller.empleado_bp)
app.register_blueprint(proveedor_controller.proveedor_bp)
app.register_blueprint(categoria_controller.categoria_bp)
app.register_blueprint(empleado_cliente_controller.empleado_cliente_bp)
app.register_blueprint(carrito_empleado_controller.carrito_empleado_bp)
app.register_blueprint(detalle_venta_controller.detalle_venta_bp)
app.register_blueprint(modelo_vehiculo_controller.modelo_vehiculo_bp)

# Context processor para navegación activa
@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active)

@app.route('/')
def home():
    if current_user.is_authenticated:
        # Redirigir según rol
        if current_user.rol == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.rol == 'empleado':
            return redirect(url_for('empleado_dashboard'))
    return redirect(url_for('login'))

# Login con Flask-Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Si ya está logueado, redirigir al dashboard
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.verify_password(password):
            login_user(usuario)  # Loguea con Flask-Login

            flash('Inicio de sesión exitoso', 'success')

            # Redirige según rol
            if usuario.rol == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif usuario.rol == 'empleado':
                return redirect(url_for('empleado_dashboard'))
            else:
                flash('Rol no válido', 'danger')
                logout_user()
                return redirect(url_for('login'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

# Dashboard admin protegido con login_required y control rol
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        flash('Acceso denegado: solo administradores', 'danger')
        return redirect(url_for('home'))
    return render_template('base.html')

# Dashboard empleado protegido con login_required y control rol
@app.route('/empleado')
@login_required
def empleado_dashboard():
    if current_user.rol != 'empleado':
        flash('Acceso denegado: solo empleados', 'danger')
        return redirect(url_for('home'))
    return render_template('empleados/base.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

# def drop_productos_table():
#     with app.app_context():
#         # Ejecutar SQL crudo para eliminar tabla si existe
#         db.session.execute(text("DROP TABLE IF EXISTS ventas;"))
#         db.session.commit()
#         print("Tabla 'ventas' eliminada si existía.")
        
if __name__ == "__main__":
    with app.app_context():
        #drop_productos_table()  # Llamar para eliminar la tabla antes de crear tablas
        db.create_all()
    app.run(debug=True)
