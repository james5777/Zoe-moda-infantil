from zoer import db
import datetime

# Cada clase hereda de db.Model y representa una tabla en SQL Server.
# Se sigue la estructura de la clase 'Niños' proporcionada.
# ==============================================================================

class Administrador(db.Model):
    """
    Modelo para la tabla 'Administrador'.
    Almacena información de los administradores del sitio.
    """
    __tablename__ = 'Administrador'
    IDAdministrador = db.Column(db.String(13), primary_key=True, nullable=False)
    NombreAdministrador = db.Column(db.String(45), nullable=False)
    ContraseñaAdministrador = db.Column(db.String(10), nullable=False)
    ApellidoAdministrador = db.Column(db.String(45), nullable=False)
    CorreoAdministrador = db.Column(db.String(45), nullable=False, unique=True) # UQ_CorreoAdminitrador
    CelularAdministrador = db.Column(db.String(10), nullable=False)
    DireccionAdministrador = db.Column(db.String(100), nullable=False)

    def __init__(self, IDAdministrador, NombreAdministrador, ContraseñaAdministrador,
                 ApellidoAdministrador, CorreoAdministrador, CelularAdministrador,
                 DireccionAdministrador):
        self.IDAdministrador = IDAdministrador
        self.NombreAdministrador = NombreAdministrador
        self.ContraseñaAdministrador = ContraseñaAdministrador
        self.ApellidoAdministrador = ApellidoAdministrador
        self.CorreoAdministrador = CorreoAdministrador
        self.CelularAdministrador = CelularAdministrador
        self.DireccionAdministrador = DireccionAdministrador

    def __repr__(self):
        return f'<Administrador {self.NombreAdministrador} {self.ApellidoAdministrador}>'

class CarritoDeCompras(db.Model):
    """
    Modelo para la tabla 'CarritoDeCompras'.
    Almacena información general de los carritos de compra de los usuarios.
    """
    __tablename__ = 'CarritoDeCompras'
    IDCarrito = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Usuario = db.Column(db.String(13), db.ForeignKey('Usuarios.IDUsuario'), nullable=False) # FK_Carrito_Usuarios
    ValorTotal = db.Column(db.Numeric(10, 4), nullable=False) # money en SQL Server
    CantProductos = db.Column(db.Integer, nullable=False)

    # Relación con la tabla Usuarios
    usuario_rel = db.relationship('Usuario', backref='carritos')
    # Relación con DetalleCarrito (un carrito puede tener muchos detalles)
    detalles_carrito = db.relationship('DetalleCarrito', backref='carrito', lazy=True)
    # Relación con Pago (un carrito puede tener un pago)
    pago_rel = db.relationship('Pago', backref='carrito_de_compras', uselist=False)

    def __init__(self, Usuario, ValorTotal, CantProductos):
        self.Usuario = Usuario
        self.ValorTotal = ValorTotal
        self.CantProductos = CantProductos

    def __repr__(self):
        return f'<Carrito {self.IDCarrito} - Usuario: {self.Usuario}>'

class Comentario(db.Model):
    """
    Modelo para la tabla 'comentarios'.
    Almacena los comentarios y calificaciones de los productos.
    """
    __tablename__ = 'comentarios' # Nombre de tabla en minúsculas en SQL script
    IDComentario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    IDUsuario = db.Column(db.String(13), db.ForeignKey('Usuarios.IDUsuario'), nullable=False) # FK_Comentario_Usuario
    IDProducto = db.Column(db.Integer, db.ForeignKey('Productos.IDProducto'), nullable=False) # FK_Comentario_Producto
    Texto = db.Column(db.String(500), nullable=False)
    Calificacion = db.Column(db.Integer, nullable=True) # NULL en SQL Server

    # Relaciones
    usuario_rel = db.relationship('Usuario', backref='comentarios')
    producto_rel = db.relationship('Producto', backref='comentarios')

    def __init__(self, IDUsuario, IDProducto, Texto, Calificacion=None):
        self.IDUsuario = IDUsuario
        self.IDProducto = IDProducto
        self.Texto = Texto
        self.Calificacion = Calificacion

    def __repr__(self):
        return f'<Comentario {self.IDComentario} - Producto: {self.IDProducto}>'

class DetalleCarrito(db.Model):
    """
    Modelo para la tabla 'DetalleCarrito'.
    Almacena los productos individuales dentro de un carrito de compras.
    """
    __tablename__ = 'DetalleCarrito'
    IDDetalleCarrito = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    IDCarrito = db.Column(db.Integer, db.ForeignKey('CarritoDeCompras.IDCarrito'), nullable=False) # FK_Carrito_DetalleCarrito
    IDProducto = db.Column(db.Integer, db.ForeignKey('Productos.IDProducto'), nullable=False) # FK_Producto_DetalleCarrito
    Cantidad = db.Column(db.Integer, nullable=False)

    # Relaciones
    carrito_rel = db.relationship('CarritoDeCompras', backref='detalles_de_carrito')
    producto_rel = db.relationship('Producto', backref='detalles_carrito')

    def __init__(self, IDCarrito, IDProducto, Cantidad):
        self.IDCarrito = IDCarrito
        self.IDProducto = IDProducto
        self.Cantidad = Cantidad

    def __repr__(self):
        return f'<DetalleCarrito {self.IDDetalleCarrito} - Carrito: {self.IDCarrito}>'

class DetallePedido(db.Model):
    """
    Modelo para la tabla 'DetallePedido'.
    Almacena los productos individuales dentro de un pedido.
    """
    __tablename__ = 'DetallePedido'
    IDDetallePedido = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    IDPedido = db.Column(db.Integer, db.ForeignKey('Pedidos.IDPedido'), nullable=False) # FK_Detalle_Pedido
    IDProducto = db.Column(db.Integer, db.ForeignKey('Productos.IDProducto'), nullable=False) # FK_Detalle_Producto
    Cantidad = db.Column(db.Integer, nullable=False)

    # Relaciones
    pedido_rel = db.relationship('Pedido', backref='detalles_de_pedido')
    producto_rel = db.relationship('Producto', backref='detalles_pedido')

    def __init__(self, IDPedido, IDProducto, Cantidad):
        self.IDPedido = IDPedido
        self.IDProducto = IDProducto
        self.Cantidad = Cantidad

    def __repr__(self):
        return f'<DetallePedido {self.IDDetallePedido} - Pedido: {self.IDPedido}>'

class Pago(db.Model):
    """
    Modelo para la tabla 'Pago'.
    Almacena información sobre los pagos realizados.
    """
    __tablename__ = 'Pago'
    IDPago = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    CarritoCompras = db.Column(db.Integer, db.ForeignKey('CarritoDeCompras.IDCarrito'), nullable=False) # FK_Pago_Carrito
    MontoPago = db.Column(db.Numeric(10, 4), nullable=False) # money en SQL Server
    MetodoPago = db.Column(db.String(40), nullable=False)
    EstadoPago = db.Column(db.Boolean, nullable=True) # bit en SQL Server, NULLable

    # Relación
    carrito_rel = db.relationship('CarritoDeCompras', backref='pagos')

    def __init__(self, CarritoCompras, MontoPago, MetodoPago, EstadoPago=None):
        self.CarritoCompras = CarritoCompras
        self.MontoPago = MontoPago
        self.MetodoPago = MetodoPago
        self.EstadoPago = EstadoPago

    def __repr__(self):
        return f'<Pago {self.IDPago} - Monto: {self.MontoPago}>'

class Pedido(db.Model):
    """
    Modelo para la tabla 'Pedidos'.
    Almacena información general de los pedidos de los usuarios.
    """
    __tablename__ = 'Pedidos'
    IDPedido = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Usuario = db.Column(db.String(13), db.ForeignKey('Usuarios.IDUsuario'), nullable=False) # FK_Pedido_Usuario
    FechaPedido = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # Puedes usar default=datetime.datetime.now
    EstadoPedido = db.Column(db.String(20), nullable=False)
    Total = db.Column(db.Numeric(10, 4), nullable=False) # money en SQL Server
    CostoEnvio = db.Column(db.Numeric(10, 4), nullable=False) # money en SQL Server

    # Relación con DetallePedido (un pedido puede tener muchos detalles)
    detalles_pedido = db.relationship('DetallePedido', backref='pedido', lazy=True)
    # Relación con Usuarios
    usuario_rel = db.relationship('Usuario', backref='pedidos')

    def __init__(self, Usuario, FechaPedido, EstadoPedido, Total, CostoEnvio):
        self.Usuario = Usuario
        self.FechaPedido = FechaPedido
        self.EstadoPedido = EstadoPedido
        self.Total = Total
        self.CostoEnvio = CostoEnvio

    def __repr__(self):
        return f'<Pedido {self.IDPedido} - Estado: {self.EstadoPedido}>'

class Producto(db.Model):
    """
    Modelo para la tabla 'Productos'.
    Almacena la información de los productos disponibles.
    """
    __tablename__ = 'Productos'
    IDProducto = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    NombreProducto = db.Column(db.String(70), nullable=False)
    DescripcionProducto = db.Column(db.String(3000), nullable=False)
    Precio = db.Column(db.Numeric(10, 4), nullable=True) # money en SQL Server, NULLable
    CantidadStock = db.Column(db.Integer, nullable=False)
    Categoria = db.Column(db.String(40), nullable=False)
    StockMax = db.Column(db.Integer, nullable=False, default=25) # DEFAULT ((25))
    StockMin = db.Column(db.Integer, nullable=False, default=25) # DEFAULT ((25))

    # Relaciones inversas con DetalleCarrito y DetallePedido
    # comentarios_rel = db.relationship('Comentario', backref='producto', lazy=True) # Ya definido en Comentario
    # detalles_carrito_rel = db.relationship('DetalleCarrito', backref='producto', lazy=True) # Ya definido en DetalleCarrito
    # detalles_pedido_rel = db.relationship('DetallePedido', backref='producto', lazy=True) # Ya definido en DetallePedido


    def __init__(self, NombreProducto, DescripcionProducto, CantidadStock, Categoria, Precio=None, StockMax=25, StockMin=25):
        self.NombreProducto = NombreProducto
        self.DescripcionProducto = DescripcionProducto
        self.Precio = Precio
        self.CantidadStock = CantidadStock
        self.Categoria = Categoria
        self.StockMax = StockMax
        self.StockMin = StockMin

    def __repr__(self):
        return f'<Producto {self.NombreProducto}>'

class Usuario(db.Model):
    """
    Modelo para la tabla 'Usuarios'.
    Almacena la información de los usuarios del sitio.
    """
    __tablename__ = 'Usuarios'
    IDUsuario = db.Column(db.String(13), primary_key=True, nullable=False)
    NombreUsuario = db.Column(db.String(45), nullable=False)
    ApellidoUsuario = db.Column(db.String(45), nullable=False)
    CorreoElectronico = db.Column(db.String(45), nullable=False, unique=True) # UQ_Correo
    Contraseña = db.Column(db.String(255), nullable=False) # NOTA: Considera un tamaño mayor para contraseñas hasheadas (ej. String(128))
    Direccion = db.Column(db.String(100), nullable=False)
    Celular = db.Column(db.String(10), nullable=False)
    Ciudad = db.Column(db.String(50), nullable=True)
    Barrio = db.Column(db.String(50), nullable=True)
    Departamento = db.Column(db.String(50), nullable=True)

    # Relaciones inversas
    # carritos_rel = db.relationship('CarritoDeCompras', backref='usuario', lazy=True) # Ya definido en CarritoDeCompras
    # comentarios_rel = db.relationship('Comentario', backref='usuario', lazy=True) # Ya definido en Comentario
    # pedidos_rel = db.relationship('Pedido', backref='usuario', lazy=True) # Ya definido en Pedido


    def __init__(self, IDUsuario, NombreUsuario, ApellidoUsuario, CorreoElectronico, Contraseña, Direccion, Celular, Ciudad=None, Barrio=None, Departamento=None    ):
        self.IDUsuario = IDUsuario
        self.NombreUsuario = NombreUsuario
        self.ApellidoUsuario = ApellidoUsuario
        self.CorreoElectronico = CorreoElectronico
        self.Contraseña = Contraseña
        self.Direccion = Direccion
        self.Celular = Celular
        self.Ciudad = Ciudad
        self.Barrio = Barrio
        self.Departamento = Departamento

    def __repr__(self):
        return f'<Usuario {self.NombreUsuario} {self.ApellidoUsuario}>'

