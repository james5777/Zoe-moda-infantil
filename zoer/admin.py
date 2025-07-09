from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g, current_app

from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import secure_filename

from .models import Producto, ImagenProducto

from zoer import db

import os

import functools



bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')



@bp.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        # Se obtienen los datos del formulario
        nombre = request.form.get('NombreProducto')
        descripcion = request.form.get('DescripcionProducto')
        precio = request.form.get('Precio')
        cantidad_stock = request.form.get('CantidadStock')
        categoria = request.form.get('Categoria')
        stock_max = request.form.get('StockMax')
        stock_min = request.form.get('StockMin')

        error = None

        #Validacion de campos
        if not nombre or not descripcion or not precio:
            error = 'el nombre, descripcion y precio son obligatorios'

        try:
            precio = float(precio)
            cantidad_stock = int(cantidad_stock)
            stock_max = int(stock_max)
            stock_min = int(stock_min)
        except (ValueError, TypeError):
            error = 'Precio, Cantidad en Stock, Stock Máximo y Mínimo deben ser números válidos.'

        #Manejo de imagenes
        uploaded_files = request.files.getlist('Imagenes_producto')
        if not uploaded_files or all(f.filename == '' for f in uploaded_files):
            error = 'Debes subir almenos una imagen para el producto.'
        elif len(uploaded_files) > 6:
            error = 'No puedes subir mas de 6 imagenes.'

        if error is None:
         #Crear Producto
            try:
                # 1. Crear y guardar el Producto primero para obtener su ID
                nuevo_producto = Producto(
                    NombreProducto=nombre,
                    DescripcionProducto=descripcion,
                    Precio=precio,
                    CantidadStock=cantidad_stock,
                    Categoria=categoria,
                    StockMax=stock_max,
                    StockMin=stock_min
                )
                db.session.add(nuevo_producto)
                db.session.flush() # Se asegura de que el id se genere

                # Guardar las imagenes del producto
                upload_folder_absolute = os.path.join(current_app.root_path, 'static', 'img')
                os.makedirs(upload_folder_absolute, exist_ok=True)

                for i, file in enumerate(uploaded_files):
                    if file and file.filename != '':
                        filename = secure_filename(file.filename)

                        unique_filename = f"prod_{nuevo_producto.IDProducto}_{i+1}_{filename}"
                        file_path_full = os.path.join(upload_folder_absolute, unique_filename)
                        file.save(file_path_full)

                        # Ruta relativa para almacenar en la base de datos
                        ruta_para_url_for = os.path.join('img', unique_filename).replace('\\', '/')

                        #Crear instancia de ImagenProducto
                        nueva_imagen = ImagenProducto(
                            IDProducto=nuevo_producto.IDProducto,
                            RutaImagen=f"static/{ruta_para_url_for}",
                            EsPrincipal=(i == 0), #La primera imagen es la principal
                            Orden=i + 1

                        )
                        db.session.add(nueva_imagen)
                
                db.session.commit()
                flash('Producto creado exitosamente.')
                return redirect(url_for('home.index'))  # Redirigir a la página de inicio o a donde desees
            
            except Exception as e:
                db.session.rollback()
                error = f'Error al crear el producto: {str(e)}'
        
        #Si hay error mostrar mensaje
        if error:
            flash(error, 'danger')
    
    return render_template('admin/crear_producto.html')




    return render_template('admin/crear_producto.html')



@bp.route('/manage_carousel')
def manage_carousel():
    return render_template('admin/manage_carousel.html')



@bp.route('/lista_productos')
def lista_productos():
    return render_template('admin/lista_productos.html')







@bp.route('/list_orders')
def list_orders():
    return render_template('admin/list_orders.html')



@bp.route('/list_users')
def list_users():
    return render_template('admin/list_users.html')

