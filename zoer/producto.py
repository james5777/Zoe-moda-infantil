from flask import Blueprint, render_template, url_for, flash,request, redirect, g
from zoer.models import Producto, ImagenProducto, Usuario
from zoer import db

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

@bp.route('/view_producto/<producto_id>')
def view_producto(producto_id):

    product = Producto.query.get_or_404(producto_id)

    images_from_db = ImagenProducto.query.filter_by(IDProducto=producto_id).order_by(ImagenProducto.EsPrincipal.desc(), ImagenProducto.Orden.asc()).all()

    producto_imagenes_urls =[]
    for img in images_from_db:
        producto_imagenes_urls.append(img.RutaImagen.replace('static/', ''))

    if not producto_imagenes_urls:
        # si no hay imagenes, usar la imagen por defecto
        producto_imagenes_urls.append(url_for('static', filename='img/default.jpg'))

    

    

    return render_template('view_producto.html', product=product, images=producto_imagenes_urls)

