from flask_login import UserMixin
from conexion.conexion import get_connection


class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = str(id_usuario)
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()

        if fila:
            return Usuario(
                fila["id_usuario"],
                fila["nombre"],
                fila["email"],
                fila["password"]
            )
        return None

    @staticmethod
    def obtener_por_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()

        if fila:
            return Usuario(
                fila["id_usuario"],
                fila["nombre"],
                fila["email"],
                fila["password"]
            )
        return None