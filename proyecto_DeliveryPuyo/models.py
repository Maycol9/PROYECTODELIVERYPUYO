from flask_login import UserMixin
from conexion.conexion import get_connection


class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id_usuario)

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s",
            (id_usuario,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Usuario(
                row["id_usuario"],
                row["nombre"],
                row["email"],
                row["password"]
            )
        return None

    @staticmethod
    def obtener_por_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s",
            (email,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Usuario(
                row["id_usuario"],
                row["nombre"],
                row["email"],
                row["password"]
            )
        return None