from sqlalchemy import func
from database import db
from models.usuario import Usuario


def obtener_usuario_por_id(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except Exception:
        return None


def obtener_usuario_por_email(email):
    if not email:
        return None
    return Usuario.query.filter(func.lower(Usuario.email) == email.lower()).first()


def registrar_usuario(usuario):
    db.session.add(usuario)
    db.session.commit()
    return usuario


def obtener_usuarios():
    return Usuario.query.order_by(Usuario.id_usuario.desc()).all()
