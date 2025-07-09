from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
# Importar las librerías necesarias
from werkzeug.security import generate_password_hash, check_password_hash

# Importar el modelo de Usuario y la base de datos
from zoer.models import Usuario, Administrador
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
        
        # ¡NUEVO CÓDIGO AQUÍ! Validar si el IDUsuario ya existe
        user_id_exists = Usuario.query.filter_by(IDUsuario=IDUsuario).first()
        if user_id_exists:
            error = 'El número de identificación (IDUsuario) ya está registrado.'

        # comparando correo electronico con los existentes
        user_email_exists = Usuario.query.filter_by(CorreoElectronico=CorreoElectronico).first()

        # ¡AJUSTE CLAVE AQUÍ!
        # Solo intentamos guardar si NO hay un error previo (por ID) Y el correo no existe.
        if error is None and user_email_exists is None:
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
                return redirect(url_for('auth.login_users'))
            except Exception as e:
                db.session.rollback()
                # Esto captura errores inesperados de la base de datos (ej. si algo más falla)
                error = f'Ocurrió un error inesperado al registrar el usuario: {str(e)}'
        else:
            # Si ya había un error por ID, o si el correo existe, el error se establece aquí.
            # Priorizamos el error de ID si ya se había detectado.
            if error is None: # Si no había error por ID, entonces el error es por el email
                error = 'El correo electrónico ya está registrado.'
            
        # Si hay un error (por validación o por excepción), mostrar un mensaje
        if error: # Solo flashear si hay un mensaje de error
            flash(error, 'danger')

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

