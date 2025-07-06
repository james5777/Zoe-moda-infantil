from flask import Blueprint, render_template

#Creo el blueprint de inicio
bp = Blueprint('auth', __name__, url_prefix='/auth')


#Vista para la pagina de registro
@bp.route('/register_users')
def register_users():
    return render_template('auth/register_users.html')

#Vista para la pagina de login
@bp.route('/login_users')
def login_users():
    return render_template('auth/login_users.html')

#Vista para la pagina de perfil
@bp.route('/profile')
def profile():
    return 'Pagina de profile'

