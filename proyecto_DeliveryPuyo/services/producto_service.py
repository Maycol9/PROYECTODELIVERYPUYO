from conexion.conexion import get_connection
from models.producto import Producto


def obtener_productos():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos ORDER BY id_producto DESC")
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()
    return productos


def obtener_producto_por_id(id_producto):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM productos WHERE id_producto = %s",
        (id_producto,)
    )
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()
    return producto


def insertar_producto(producto: Producto):
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO productos (nombre, categoria, precio, stock)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        producto.nombre,
        producto.categoria,
        producto.precio,
        producto.stock
    )

    cursor.execute(sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def actualizar_producto(producto: Producto):
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        UPDATE productos
        SET nombre = %s, categoria = %s, precio = %s, stock = %s
        WHERE id_producto = %s
    """
    valores = (
        producto.nombre,
        producto.categoria,
        producto.precio,
        producto.stock,
        producto.id_producto
    )

    cursor.execute(sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminar_producto(id_producto):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id_producto = %s",
        (id_producto,)
    )
    conexion.commit()

    cursor.close()
    conexion.close()