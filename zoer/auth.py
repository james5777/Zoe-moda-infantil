from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
# Importar las librerías necesarias
from werkzeug.security import generate_password_hash, check_password_hash

# Importar el modelo de Usuario y la base de datos
from zoer.models import Usuario
from zoer import db

# Importar functools para el decorador
import functools

#Creo el blueprint de inicio
bp = Blueprint('auth', __name__, url_prefix='/auth')


#Vista para la pagina de registro
@bp.route('/register_users' , methods=['GET', 'POST'])
def register_users():
    """Vista para registrar un nuevo usuario.
    Si el método es POST, procesa el formulario de registro."""

    if request.method == 'POST':
        # Obtener los datos del formulario
        IDUsuario = request.form.get('IDUsuario')
        NombreUsuario = request.form.get('NombreUsuario')
        ApellidoUsuario = request.form.get('ApellidoUsuario')
        CorreoElectronico = request.form.get('CorreoElectronico')
        Contraseña = request.form.get('Contraseña')
        Direccion = request.form.get('Direccion')
        Barrio = request.form.get('Barrio')
        Ciudad = request.form.get('Ciudad')
        Departamento = request.form.get('Departamento')
        Celular = request.form.get('Celular')

        user = Usuario(IDUsuario, NombreUsuario, ApellidoUsuario, CorreoElectronico, generate_password_hash(Contraseña), Direccion, Celular, Ciudad, Barrio, Departamento)

        # validacion de datos

        error = None

        #comparando correo electronico con los existentes
        user_email = Usuario.query.filter_by(CorreoElectronico=CorreoElectronico).first()

        if user_email == None:
            # Guardar el usuario en la base de datos
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login_users'))
        else:
            error = 'El correo electronico ya esta registrado'
        # Si hay un error, mostrar un mensaje
        flash(error)

    return render_template('auth/register_users.html')

#Vista para la pagina de login
@bp.route('/login_users' , methods=['GET', 'POST'])
def login_users():
    """Vista para iniciar sesión del usuario.
    Si el usuario ya está autenticado, redirige a la página de inicio."""
    if request.method == 'POST':
        CorreoElectronico = request.form.get('CorreoElectronico')
        Contraseña = request.form.get('Contraseña')

        error = None
        # Verificar si el usuario existe
        user = Usuario.query.filter_by(CorreoElectronico=CorreoElectronico).first()

        if user is None or not check_password_hash(user.Contraseña, Contraseña):
            error = 'Correo electronico o contraseña incorrectos'
        
        # Si no hay error, iniciar sesión
        if error is None:
            session.clear()
            session['user_id'] = user.IDUsuario
            return redirect(url_for('home.index'))
        
        flash(error)
    # Si el método es GET, simplemente renderizar la plantilla de login
    return render_template('auth/login_users.html')

@bp.route('/login_admins')
def login_admins():
    return render_template('auth/login_admins.html')


# mantener al usuario logueado durante la sesión
@bp.before_app_request
def load_logged_in_user():
    """Función que se ejecuta antes de cada solicitud para cargar el usuario autenticado en g.user.
    Esto permite acceder al usuario en las vistas y funciones de la aplicación."""
    user_id = session.get('user_id')
    # Verificar si el usuario está en la sesión
    # Si no hay un usuario en la sesión, g.user será None
    if user_id is None:
        g.user = None
    else:
        # Si hay un usuario en la sesión, cargarlo desde la base de datos
        # Esto permite acceder al usuario en las vistas y funciones de la aplicación
        g.user = Usuario.query.get(user_id)

@bp.route('/logout')
def logout():
    """Vista para cerrar sesión del usuario.
    Limpia la sesión y redirige a la página de inicio."""
    # Limpiar la sesión para cerrar la sesión del usuario
    session.clear()
    return redirect(url_for('home.index'))

def login_required(view):
    """
    Decorador para requerir que un usuario esté autenticado para acceder a una vista.
    Si el usuario no está autenticado, redirige a la página de inicio de sesión.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_users'))
        return view(**kwargs)
    return wrapped_view


#Vista para la pagina de perfil
@bp.route('/profile')
def profile():
    return 'Pagina de profile'

