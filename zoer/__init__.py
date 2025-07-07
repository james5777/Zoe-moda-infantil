from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # Inicializar la instancia de SQLAlchemy
# migrate = Migrate()  # Inicializar la instancia de Flask-Migrate


def create_app():   
    #Crear aplicacion
    app = Flask(__name__)

    app.config.from_object('config.Config')  # Cargar configuracion desde el archivo config.py
    db.init_app(app)  # Inicializar la instancia de SQLAlchemy con la aplicacion

    #Registrar blueprints - vistas

    #importar vitas de home
    from zoer import home
    app.register_blueprint(home.bp)

    #importar vistas de auth
    from zoer import auth
    app.register_blueprint(auth.bp)

    #importar vistas de productos
    from zoer import producto #
    app.register_blueprint(producto.bp) # productos.bp aqui se refiere al blueprint definido en productos.py es el argumento que se pasa al registrar el blueprint, el pri


    #Importar vistas de admin
    from zoer import admin
    app.register_blueprint(admin.bp)

    from zoer import models  # Importar modelos para que se registren en la base de datos

    with app.app_context():
        db.create_all()

    
    



    return app

