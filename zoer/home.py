from flask import Blueprint, render_template, url_for
from zoer.models import Producto, ImagenProducto

#Creo el blueprint de inicio
bp = Blueprint('home', __name__, static_folder='static')

@bp.route('/')
def index():

    #Obtener productos de la base de datos
    productos = Producto.query.all()
    
    productos_con_imagenes = []
    for producto in productos:

        #Obtener primera imagen del producto
        imagen_para_mostrar = ImagenProducto.query.filter_by(IDProducto=producto.IDProducto, EsPrincipal=True).first()

         # Si la RutaImagen en DB es "static/img/...", queremos solo "img/..." para url_for.
        imagen_url_para_plantilla = ""
        if imagen_para_mostrar:
            imagen_url_para_plantilla = imagen_para_mostrar.RutaImagen.replace('static/', '')
        else:
            # Si no hay imagen, usamos la imagen por defecto (ruta relativa a static)
            imagen_url_para_plantilla = 'img/default.jpg'

        productos_con_imagenes.append({
            'producto' : producto,
            'imagen_url' : imagen_url_para_plantilla # Pasa la URL de la imagen (real o por defecto)
        })

 
    return render_template('index.html', productos=productos_con_imagenes)

