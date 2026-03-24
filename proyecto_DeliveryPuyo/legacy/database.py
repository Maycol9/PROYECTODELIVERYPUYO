from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductoSQLite(db.Model):
    __tablename__ = "productos_sqlite"

    id = db.Column(db.Integer, primary_key=True)
    mysql_id = db.Column(db.Integer, unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "mysql_id": self.mysql_id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }