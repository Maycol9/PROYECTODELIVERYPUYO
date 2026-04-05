New-Item -ItemType Directory -Force -Path "forms","models","services","respaldos","static\reportes" | Out-Null

@'
Flask==3.1.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
mysql-connector-python==9.2.0
gunicorn==23.0.0
python-dotenv==1.0.1
fpdf==1.7.2
Werkzeug==3.1.3
'@ | Set-Content -Encoding UTF8 "requirements.txt"

@'
.venv/
venv/
__pycache__/
*.pyc
.env
instance/
respaldos/
static/reportes/
*.db
*.sqlite3
'@ | Set-Content -Encoding UTF8 ".gitignore"

@'
3.13.5
'@ | Set-Content -Encoding UTF8 ".python-version"

@'
SECRET_KEY=pon_una_clave_larga_y_segura
FLASK_DEBUG=True

# Opción 1: usar una URL completa
# MYSQL_URL=mysql://usuario:password@host:puerto/base

# Opción 2: usar variables separadas
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
'@ | Set-Content -Encoding UTF8 ".env.example"

@'
import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _normalize_uri(uri: str) -> str:
    if uri.startswith("mysql://"):
        return uri.replace("mysql://", "mysql+mysqlconnector://", 1)
    return uri


def get_database_uri() -> str:
    direct_uri = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
        or os.getenv("MYSQL_URL")
    )

    if direct_uri:
        return _normalize_uri(direct_uri)

    host = os.getenv("DB_HOST") or os.getenv("MYSQLHOST")
    port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT")
    user = os.getenv("DB_USER") or os.getenv("MYSQLUSER")
    password = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD")
    database = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE")

    if host and user and database:
        password = quote_plus(password or "")
        port = port or "3306"
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    return f"sqlite:///{os.path.join(base_dir, 'delivery_puyo.db')}"
'@ | Set-Content -Encoding UTF8 "database.py"

@'
from database import db
from models.usuario import Usuario
from models.producto import Producto

__all__ = ["db", "Usuario", "Producto"]
'@ | Set-Content -Encoding UTF8 "models\__init__.py"

@'
from flask_login import UserMixin
from database import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.id_usuario)

    def __repr__(self):
        return f"<Usuario {self.email}>"
'@ | Set-Content -Encoding UTF8 "models\usuario.py"

@'
from database import db


class Producto(db.Model):
    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": float(self.precio),
            "stock": self.stock
        }

    def __repr__(self):
        return f"<Producto {self.nombre}>"
'@ | Set-Content -Encoding UTF8 "models\producto.py"

@'
# forms package
'@ | Set-Content -Encoding UTF8 "forms\__init__.py"

@'
class LoginForm:
    def __init__(self, form_data):
        self.email = (form_data.get("email", "") or "").strip().lower()
        self.password = (form_data.get("password", "") or "").strip()
        self.errores = []

    def validar(self):
        self.errores = []

        if not self.email:
            self.errores.append("El correo electrónico es obligatorio.")
        if not self.password:
            self.errores.append("La contraseña es obligatoria.")

        return len(self.errores) == 0
'@ | Set-Content -Encoding UTF8 "forms\login_form.py"

@'
class RegistroForm:
    def __init__(self, form_data):
        self.nombre = (form_data.get("nombre", "") or "").strip()
        self.email = (form_data.get("email", "") or "").strip().lower()
        self.password = (form_data.get("password", "") or "").strip()
        self.confirmar_password = (form_data.get("confirmar_password", "") or "").strip()
        self.errores = []

    def validar(self):
        self.errores = []

        if not self.nombre:
            self.errores.append("El nombre es obligatorio.")
        if not self.email:
            self.errores.append("El correo electrónico es obligatorio.")
        if not self.password:
            self.errores.append("La contraseña es obligatoria.")
        if len(self.password) < 6:
            self.errores.append("La contraseña debe tener al menos 6 caracteres.")

        if self.confirmar_password and self.password != self.confirmar_password:
            self.errores.append("La confirmación de contraseña no coincide.")

        return len(self.errores) == 0
'@ | Set-Content -Encoding UTF8 "forms\registro_form.py"

@'
class ProductoForm:
    def __init__(self, form_data):
        self.nombre = (form_data.get("nombre", "") or "").strip()
        self.categoria = (form_data.get("categoria", "") or "").strip()
        self.precio = (form_data.get("precio", "") or "").strip().replace(",", ".")
        self.stock = (form_data.get("stock", "") or "").strip()
        self.errores = []

    def validar(self):
        self.errores = []

        if not self.nombre:
            self.errores.append("El nombre del producto es obligatorio.")
        if not self.categoria:
            self.errores.append("La categoría es obligatoria.")

        try:
            precio_valor = float(self.precio)
            if precio_valor < 0:
                self.errores.append("El precio no puede ser negativo.")
        except ValueError:
            self.errores.append("El precio debe ser numérico.")

        try:
            stock_valor = int(self.stock)
            if stock_valor < 0:
                self.errores.append("El stock no puede ser negativo.")
        except ValueError:
            self.errores.append("El stock debe ser un número entero.")

        return len(self.errores) == 0
'@ | Set-Content -Encoding UTF8 "forms\producto_form.py"

@'
# services package
'@ | Set-Content -Encoding UTF8 "services\__init__.py"

@'
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
'@ | Set-Content -Encoding UTF8 "services\usuario_service.py"

@'
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
'@ | Set-Content -Encoding UTF8 "services\producto_service.py"

@'
import os
from fpdf import FPDF


def texto_seguro(valor):
    return str(valor).encode("latin-1", "replace").decode("latin-1")


def _valor(producto, campo, default=""):
    if isinstance(producto, dict):
        return producto.get(campo, default)
    return getattr(producto, campo, default)


def generar_pdf_productos(productos, ruta_archivo):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, texto_seguro("Reporte de Productos - DeliverPuyo"), 0, 1, "C")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        190,
        8,
        texto_seguro("Resumen del catálogo de productos registrados en la plataforma."),
        0,
        1,
        "C"
    )

    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(15, 8, "ID", 1, 0, "C")
    pdf.cell(60, 8, texto_seguro("Nombre"), 1, 0, "C")
    pdf.cell(45, 8, texto_seguro("Categoría"), 1, 0, "C")
    pdf.cell(30, 8, texto_seguro("Precio"), 1, 0, "C")
    pdf.cell(25, 8, "Stock", 1, 1, "C")

    pdf.set_font("Helvetica", "", 9)

    if not productos:
        pdf.cell(175, 8, texto_seguro("No existen productos registrados."), 1, 1, "C")
    else:
        for producto in productos:
            pdf.cell(15, 8, texto_seguro(_valor(producto, "id_producto", "")), 1, 0, "C")
            pdf.cell(60, 8, texto_seguro(_valor(producto, "nombre", ""))[:30], 1, 0, "L")
            pdf.cell(45, 8, texto_seguro(_valor(producto, "categoria", ""))[:22], 1, 0, "L")
            pdf.cell(30, 8, texto_seguro(f"$ {_valor(producto, 'precio', 0)}"), 1, 0, "R")
            pdf.cell(25, 8, texto_seguro(_valor(producto, "stock", 0)), 1, 1, "C")

    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    pdf.output(ruta_archivo)
'@ | Set-Content -Encoding UTF8 "services\reporte_service.py"

@'
import csv
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESPALDOS_DIR = BASE_DIR / "respaldos"
TXT_FILE = RESPALDOS_DIR / "productos.txt"
JSON_FILE = RESPALDOS_DIR / "productos.json"
CSV_FILE = RESPALDOS_DIR / "productos.csv"
SQLITE_FILE = RESPALDOS_DIR / "productos_respaldo.db"


def _producto_a_dict(producto):
    if isinstance(producto, dict):
        return {
            "id_producto": producto.get("id_producto"),
            "nombre": producto.get("nombre"),
            "categoria": producto.get("categoria"),
            "precio": float(producto.get("precio", 0)),
            "stock": int(producto.get("stock", 0))
        }

    if hasattr(producto, "to_dict"):
        return producto.to_dict()

    return {
        "id_producto": getattr(producto, "id_producto", None),
        "nombre": getattr(producto, "nombre", ""),
        "categoria": getattr(producto, "categoria", ""),
        "precio": float(getattr(producto, "precio", 0)),
        "stock": int(getattr(producto, "stock", 0))
    }


def init_local_files():
    RESPALDOS_DIR.mkdir(parents=True, exist_ok=True)

    if not TXT_FILE.exists():
        TXT_FILE.write_text("", encoding="utf-8")

    if not JSON_FILE.exists():
        JSON_FILE.write_text("[]", encoding="utf-8")

    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id_producto", "nombre", "categoria", "precio", "stock"]
            )
            writer.writeheader()

    conn = sqlite3.connect(SQLITE_FILE)
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()


def sincronizar_persistencia(productos):
    init_local_files()
    productos_list = [_producto_a_dict(p) for p in productos]

    lineas = []
    for p in productos_list:
        lineas.append(
            f"ID: {p['id_producto']} | Nombre: {p['nombre']} | "
            f"Categoría: {p['categoria']} | Precio: {p['precio']} | Stock: {p['stock']}"
        )

    TXT_FILE.write_text("\n".join(lineas), encoding="utf-8")
    JSON_FILE.write_text(json.dumps(productos_list, ensure_ascii=False, indent=2), encoding="utf-8")

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id_producto", "nombre", "categoria", "precio", "stock"]
        )
        writer.writeheader()
        writer.writerows(productos_list)

    conn = sqlite3.connect(SQLITE_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM productos")
    cur.executemany(
        '''
        INSERT INTO productos (id_producto, nombre, categoria, precio, stock)
        VALUES (?, ?, ?, ?, ?)
        ''',
        [
            (
                p["id_producto"],
                p["nombre"],
                p["categoria"],
                p["precio"],
                p["stock"]
            )
            for p in productos_list
        ]
    )
    conn.commit()
    conn.close()


def leer_txt():
    init_local_files()
    return TXT_FILE.read_text(encoding="utf-8")


def leer_json():
    init_local_files()
    try:
        data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        return "[]"


def leer_csv():
    init_local_files()
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def leer_sqlite():
    init_local_files()
    conn = sqlite3.connect(SQLITE_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos ORDER BY id_producto DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows
'@ | Set-Content -Encoding UTF8 "services\persistencia_service.py"

@'
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database import db, get_database_uri
from models.usuario import Usuario
from models.producto import Producto

from forms.login_form import LoginForm
from forms.registro_form import RegistroForm
from forms.producto_form import ProductoForm

from services.usuario_service import (
    obtener_usuario_por_id,
    obtener_usuario_por_email,
    registrar_usuario,
    obtener_usuarios
)

from services.producto_service import (
    obtener_productos,
    obtener_producto_por_id,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

from services.reporte_service import generar_pdf_productos
from services.persistencia_service import (
    init_local_files,
    sincronizar_persistencia,
    leer_txt,
    leer_json,
    leer_csv,
    leer_sqlite
)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static"
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "deliverpuyo_secret_key_2026")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Debes iniciar sesión para acceder al panel de DeliverPuyo."
    login_manager.login_message_category = "warning"

    with app.app_context():
        db.create_all()
        init_local_files()
        try:
            sincronizar_persistencia(obtener_productos())
        except Exception as e:
            print(f"Error al inicializar los respaldos de DeliverPuyo: {e}")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/nosotros")
    def nosotros():
        return render_template("nosotros.html")

    @app.route("/cliente/<nombre>")
    def cliente(nombre):
        return f"Hola, {nombre}. Bienvenido a DeliverPuyo. Tu solicitud está siendo procesada correctamente."

    @app.route("/zona/<sector>")
    def zona(sector):
        return f"DeliverPuyo mantiene cobertura operativa y gestión de pedidos en el sector: {sector}."

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            form = RegistroForm(request.form)

            if form.validar():
                usuario_existente = obtener_usuario_por_email(form.email)

                if usuario_existente:
                    flash("El correo ingresado ya se encuentra registrado en DeliverPuyo.", "danger")
                else:
                    password_hash = generate_password_hash(form.password)

                    nuevo_usuario = Usuario(
                        nombre=form.nombre,
                        email=form.email,
                        password=password_hash
                    )

                    registrar_usuario(nuevo_usuario)
                    flash("Tu cuenta fue creada correctamente. Ahora puedes iniciar sesión en DeliverPuyo.", "success")
                    return redirect(url_for("login"))
            else:
                for error in form.errores:
                    flash(error, "danger")

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            form = LoginForm(request.form)

            if form.validar():
                usuario = obtener_usuario_por_email(form.email)

                if usuario and check_password_hash(usuario.password, form.password):
                    login_user(usuario)
                    flash(f"Bienvenido, {usuario.nombre}. Has ingresado correctamente a DeliverPuyo.", "success")
                    return redirect(url_for("dashboard"))
                else:
                    flash("No fue posible iniciar sesión. Verifica tu correo y contraseña.", "danger")
            else:
                for error in form.errores:
                    flash(error, "danger")

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Has cerrado sesión correctamente en DeliverPuyo.", "info")
        return redirect(url_for("login"))

    @app.route("/usuarios")
    @login_required
    def usuarios():
        lista_usuarios = obtener_usuarios()
        return render_template("usuarios.html", usuarios=lista_usuarios)

    @app.route("/productos")
    @login_required
    def listar_productos():
        productos = [p.to_dict() for p in obtener_productos()]
        return render_template("productos/listar.html", productos=productos)

    @app.route("/productos/crear", methods=["GET", "POST"])
    @login_required
    def crear_producto():
        if request.method == "POST":
            form = ProductoForm(request.form)

            if form.validar():
                producto = Producto(
                    nombre=form.nombre,
                    categoria=form.categoria,
                    precio=float(form.precio),
                    stock=int(form.stock)
                )

                insertar_producto(producto)
                sincronizar_persistencia(obtener_productos())

                flash("El producto fue registrado correctamente en el catálogo de DeliverPuyo.", "success")
                return redirect(url_for("listar_productos"))
            else:
                for error in form.errores:
                    flash(error, "danger")

        return render_template("productos/crear.html")

    @app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
    @login_required
    def editar_producto(id_producto):
        producto_db = obtener_producto_por_id(id_producto)

        if not producto_db:
            flash("El producto solicitado no fue encontrado en DeliverPuyo.", "warning")
            return redirect(url_for("listar_productos"))

        if request.method == "POST":
            form = ProductoForm(request.form)

            if form.validar():
                producto = Producto(
                    id_producto=id_producto,
                    nombre=form.nombre,
                    categoria=form.categoria,
                    precio=float(form.precio),
                    stock=int(form.stock)
                )

                actualizar_producto(producto)
                sincronizar_persistencia(obtener_productos())

                flash("La información del producto fue actualizada correctamente.", "success")
                return redirect(url_for("listar_productos"))
            else:
                for error in form.errores:
                    flash(error, "danger")

        return render_template("productos/editar.html", producto=producto_db.to_dict())

    @app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
    @login_required
    def eliminar_producto_route(id_producto):
        producto_db = obtener_producto_por_id(id_producto)

        if not producto_db:
            flash("No fue posible eliminar el producto porque no existe en el sistema.", "warning")
        else:
            eliminar_producto(id_producto)
            sincronizar_persistencia(obtener_productos())
            flash("El producto fue eliminado correctamente del catálogo de DeliverPuyo.", "success")

        return redirect(url_for("listar_productos"))

    @app.route("/productos/pdf")
    @login_required
    def reporte_productos_pdf():
        productos = obtener_productos()

        carpeta_reportes = os.path.join(app.root_path, "static", "reportes")
        os.makedirs(carpeta_reportes, exist_ok=True)

        ruta_pdf = os.path.join(carpeta_reportes, "reporte_productos.pdf")
        generar_pdf_productos(productos, ruta_pdf)

        return send_file(
            ruta_pdf,
            as_attachment=True,
            download_name="reporte_productos_deliverpuyo.pdf"
        )

    @app.route("/datos")
    @login_required
    def datos():
        productos = obtener_productos()
        sincronizar_persistencia(productos)

        return render_template(
            "datos.html",
            datos_txt=leer_txt(),
            datos_json=leer_json(),
            datos_csv=leer_csv(),
            datos_sqlite=leer_sqlite()
        )

    return app


app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
'@ | Set-Content -Encoding UTF8 "app.py"

Write-Host ""
Write-Host "Archivos corregidos y creados correctamente." -ForegroundColor Green
Write-Host "Ahora instala dependencias y prueba con: python app.py" -ForegroundColor Cyan
