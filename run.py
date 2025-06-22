from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from controllers import usuario_controller, cliente_controller, producto_controller, venta_controller
from models.usuario_model import Usuario  # Importa tu modelo Usuario
from database import db

app = Flask(__name__)
app.secret_key = 'clave-secreta-123'  # Necesaria para usar sesiones

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)

# Context processor para navegación activa
@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active)

# Ruta raíz redirige a login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.verify_password(password):
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.rol

            if usuario.rol == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif usuario.rol == 'empleado':
                return redirect(url_for('empleado_dashboard'))
            else:
                flash('Rol no válido', 'danger')
        else:
            flash('Usuario o contraseña incorrectos', 'error')


    return render_template('login.html')

# Ruta de dashboard para administrador
@app.route('/admin')
def admin_dashboard():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        flash('Acceso denegado: Admin solo', 'danger')
        return redirect(url_for('login'))
    return render_template('usuarios/index.html')

# Ruta de dashboard para empleado
@app.route('/empleado')
def empleado_dashboard():
    if 'usuario_id' not in session or session.get('rol') != 'empleado':
        flash('Acceso denegado: Empleado solo', 'danger')
        return redirect(url_for('login'))
    return render_template('empleado/dashboard.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
