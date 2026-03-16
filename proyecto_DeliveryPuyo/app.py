import os
import json
import csv

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_connection
from models import Usuario
from database import db, ProductoSQLite


app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "deliverpuyo_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///delivery_puyo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta sección."


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "inventario", "data")
TXT_FILE = os.path.join(DATA_DIR, "datos.txt")
JSON_FILE = os.path.join(DATA_DIR, "datos.json")
CSV_FILE = os.path.join(DATA_DIR, "datos.csv")


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)


def init_local_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8"):
            pass

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id_producto", "nombre", "categoria", "precio", "stock"])


def obtener_productos_mysql():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_producto, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id_producto DESC
    """)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    for producto in productos:
        producto["precio"] = float(producto["precio"])
        producto["stock"] = int(producto["stock"])
        producto["id_producto"] = int(producto["id_producto"])

    return productos


def leer_txt():
    datos = []
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    partes = linea.split("|")
                    if len(partes) == 5:
                        datos.append({
                            "id_producto": partes[0],
                            "nombre": partes[1],
                            "categoria": partes[2],
                            "precio": partes[3],
                            "stock": partes[4]
                        })
    return datos


def leer_json():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def leer_csv():
    datos = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                datos.append(fila)
    return datos


def sincronizar_persistencia():
    productos = obtener_productos_mysql()

    with open(TXT_FILE, "w", encoding="utf-8") as f:
        for p in productos:
            f.write(f"{p['id_producto']}|{p['nombre']}|{p['categoria']}|{p['precio']}|{p['stock']}\n")

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=4)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id_producto", "nombre", "categoria", "precio", "stock"]
        )
        writer.writeheader()
        writer.writerows(productos)

    ProductoSQLite.query.delete()
    db.session.commit()

    for p in productos:
        db.session.add(
            ProductoSQLite(
                mysql_id=p["id_producto"],
                nombre=p["nombre"],
                categoria=p["categoria"],
                precio=p["precio"],
                stock=p["stock"]
            )
        )
    db.session.commit()


with app.app_context():
    db.create_all()
    init_local_files()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/cliente/<nombre>")
def cliente(nombre):
    return f"Bienvenido, {nombre}. Tu pedido en DeliverPuyo está en proceso."


@app.route("/zona/<sector>")
def zona(sector):
    return f"DeliverPuyo realiza entregas en el sector: {sector}."


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for("register"))

        if Usuario.obtener_por_email(email):
            flash("Ese correo ya está registrado.")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Usuario registrado correctamente. Ahora inicia sesión.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        usuario = Usuario.obtener_por_email(email)

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash("Inicio de sesión exitoso.")
            return redirect(url_for("dashboard"))

        flash("Correo o contraseña incorrectos.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", usuario=current_user)


@app.route("/usuarios")
@login_required
def usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, email FROM usuarios ORDER BY id_usuario DESC")
    lista_usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("usuarios.html", usuarios=lista_usuarios)


@app.route("/productos")
@login_required
def productos():
    lista_productos = obtener_productos_mysql()
    return render_template("productos.html", productos=lista_productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()

        if not nombre or not categoria or not precio or not stock:
            flash("Todos los campos del producto son obligatorios.")
            return redirect(url_for("nuevo_producto"))

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            flash("Precio o stock inválidos.")
            return redirect(url_for("nuevo_producto"))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, categoria, precio, stock)
        )
        conn.commit()
        cursor.close()
        conn.close()

        sincronizar_persistencia()

        flash("Producto agregado correctamente.")
        return redirect(url_for("productos"))

    return render_template("producto_form.html", producto=None)


@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()

        if not nombre or not categoria or not precio or not stock:
            flash("Todos los campos del producto son obligatorios.")
            cursor.close()
            conn.close()
            return redirect(url_for("editar_producto", id_producto=id_producto))

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            flash("Precio o stock inválidos.")
            cursor.close()
            conn.close()
            return redirect(url_for("editar_producto", id_producto=id_producto))

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s, categoria = %s, precio = %s, stock = %s
            WHERE id_producto = %s
            """,
            (nombre, categoria, precio, stock, id_producto)
        )
        conn.commit()
        cursor.close()
        conn.close()

        sincronizar_persistencia()

        flash("Producto actualizado correctamente.")
        return redirect(url_for("productos"))

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if not producto:
        flash("Producto no encontrado.")
        return redirect(url_for("productos"))

    return render_template("producto_form.html", producto=producto)


@app.route("/productos/eliminar/<int:id_producto>")
@login_required
def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()

    sincronizar_persistencia()

    flash("Producto eliminado correctamente.")
    return redirect(url_for("productos"))


@app.route("/datos")
@login_required
def datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    datos_sqlite = ProductoSQLite.query.order_by(ProductoSQLite.mysql_id.desc()).all()

    return render_template(
        "datos.html",
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv,
        datos_sqlite=datos_sqlite
    )


if __name__ == "__main__":
    app.run(debug=True)