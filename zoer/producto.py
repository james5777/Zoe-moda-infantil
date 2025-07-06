from flask import Blueprint

#Creo el blueprint de inicio
bp = Blueprint('producto', __name__, url_prefix='/productos')


#Vista para la pagina de productos
@bp.route('/productos')
def productos():
    return 'Pagina de productos'

#Vista para la pagina de crear productos
@bp.route('/crear_producto')
def crear_producto():
    return 'Pagina de crear productos'

#Vista para la pagina de editar productos
@bp.route('/editar_producto')
def editar_producto():
    return 'Pagina de editar producto'

