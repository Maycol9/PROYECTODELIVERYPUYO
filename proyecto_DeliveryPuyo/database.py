import sqlite3

# --- REQUISITO: CLASE PRODUCTO ---
class Producto:
    def __init__(self, id_prod, nombre, precio, stock):
        self.id = id_prod
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "precio": self.precio, "stock": self.stock}

# --- REQUISITO: CLASE INVENTARIO (CON SQLITE Y COLECCIONES) ---
class Inventario:
    def __init__(self):
        self.db_name = "delivery_puyo.db"
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        conn = self.conectar()
        cursor = conn.cursor()
        # Crear tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           nombre TEXT NOT NULL, 
                           precio REAL NOT NULL, 
                           stock INTEGER NOT NULL)''')
        conn.commit()
        conn.close()

    # MÉTODO: AÑADIR (CRUD)
    def añadir_producto(self, nombre, precio, stock):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", 
                       (nombre, precio, stock))
        conn.commit()
        conn.close()

    # MÉTODO: MOSTRAR TODO (Uso de LISTAS y DICCIONARIOS)
    def obtener_todos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        
        # Usamos una LISTA de objetos/diccionarios (Colección)
        inventario_lista = []
        for f in filas:
            p = Producto(f[0], f[1], f[2], f[3])
            inventario_lista.append(p.to_dict())
        
        conn.close()
        return inventario_lista

    # MÉTODO: ELIMINAR POR ID
    def eliminar_producto(self, id_prod):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
        conn.commit()
        conn.close()