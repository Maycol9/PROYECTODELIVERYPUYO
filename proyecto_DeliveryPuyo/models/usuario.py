from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self, id_usuario=None, nombre="", email="", password=""):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id_usuario)