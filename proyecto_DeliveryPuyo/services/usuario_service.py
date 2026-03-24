from conexion.conexion import get_connection
from models.usuario import Usuario


def obtener_usuario_por_id(id_usuario):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s",
        (id_usuario,)
    )
    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila:
        return Usuario(
            id_usuario=fila["id_usuario"],
            nombre=fila["nombre"],
            email=fila["email"],
            password=fila["password"]
        )
    return None


def obtener_usuario_por_email(email):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s",
        (email,)
    )
    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila:
        return Usuario(
            id_usuario=fila["id_usuario"],
            nombre=fila["nombre"],
            email=fila["email"],
            password=fila["password"]
        )
    return None


def registrar_usuario(usuario):
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO usuarios (nombre, email, password)
        VALUES (%s, %s, %s)
    """
    valores = (usuario.nombre, usuario.email, usuario.password)

    cursor.execute(sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def obtener_usuarios():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_usuario, nombre, email FROM usuarios ORDER BY id_usuario DESC"
    )
    usuarios = cursor.fetchall()

    cursor.close()
    conexion.close()
    return usuarios