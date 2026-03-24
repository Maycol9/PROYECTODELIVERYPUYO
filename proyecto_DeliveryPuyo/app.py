import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
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

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "deliverpuyo_secret_key_2026")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.root_path, 'delivery_puyo.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder al panel de DeliverPuyo."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


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
    productos = obtener_productos()
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

    return render_template("productos/editar.html", producto=producto_db)


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


if __name__ == "__main__":
    app.run(debug=True)