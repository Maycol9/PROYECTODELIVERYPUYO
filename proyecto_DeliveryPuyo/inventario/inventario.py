import os
import sqlite3
from inventario.productos import Producto


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "delivery_puyo.db")


class Inventario:
    def __init__(self):
        self.productos = {}
        self.crear_tabla()
        self.cargar_productos()

    def conectar(self):
        return sqlite3.connect(DB_FILE)

    def crear_tabla(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos_inventario (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def cargar_productos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad, precio, categoria FROM productos_inventario")
        registros = cursor.fetchall()
        conn.close()

        self.productos = {}
        for fila in registros:
            producto = Producto(fila[0], fila[1], fila[2], fila[3], fila[4])
            self.productos[producto.get_id_producto()] = producto

    def agregar_producto(self, producto):
        if producto.get_id_producto() in self.productos:
            return False

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos_inventario (id, nombre, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, (
            producto.get_id_producto(),
            producto.get_nombre(),
            producto.get_cantidad(),
            producto.get_precio(),
            producto.get_categoria()
        ))
        conn.commit()
        conn.close()

        self.productos[producto.get_id_producto()] = producto
        return True

    def eliminar_producto(self, id_producto):
        if id_producto not in self.productos:
            return False

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos_inventario WHERE id = ?", (id_producto,))
        conn.commit()
        conn.close()

        del self.productos[id_producto]
        return True

    def actualizar_producto(self, id_producto, nueva_cantidad, nuevo_precio):
        if id_producto not in self.productos:
            return False

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos_inventario
            SET cantidad = ?, precio = ?
            WHERE id = ?
        """, (nueva_cantidad, nuevo_precio, id_producto))
        conn.commit()
        conn.close()

        self.productos[id_producto].set_cantidad(nueva_cantidad)
        self.productos[id_producto].set_precio(nuevo_precio)
        return True

    def buscar_por_nombre(self, nombre):
        resultados = []
        for producto in self.productos.values():
            if nombre.lower() in producto.get_nombre().lower():
                resultados.append(producto)
        return resultados

    def mostrar_todos(self):
        return list(self.productos.values())

    def obtener_categorias_unicas(self):
        return {producto.get_categoria() for producto in self.productos.values()}

    def resumen_producto(self, id_producto):
        if id_producto in self.productos:
            p = self.productos[id_producto]
            return (p.get_nombre(), p.get_cantidad(), p.get_precio())
        return None