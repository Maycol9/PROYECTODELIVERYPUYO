from database import db
from models.producto import Producto


def obtener_productos():
    return Producto.query.order_by(Producto.id_producto.desc()).all()


def obtener_producto_por_id(id_producto):
    return db.session.get(Producto, id_producto)


def insertar_producto(producto):
    db.session.add(producto)
    db.session.commit()
    return producto


def actualizar_producto(producto):
    producto_db = db.session.get(Producto, producto.id_producto)

    if not producto_db:
        return None

    producto_db.nombre = producto.nombre
    producto_db.categoria = producto.categoria
    producto_db.precio = producto.precio
    producto_db.stock = producto.stock

    db.session.commit()
    return producto_db


def eliminar_producto(id_producto):
    producto_db = db.session.get(Producto, id_producto)

    if not producto_db:
        return False

    db.session.delete(producto_db)
    db.session.commit()
    return True
