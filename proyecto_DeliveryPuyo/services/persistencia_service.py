import csv
import json
from decimal import Decimal
from pathlib import Path

from database import db, ProductoSQLite

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "respaldos"

TXT_FILE = DATA_DIR / "productos.txt"
JSON_FILE = DATA_DIR / "productos.json"
CSV_FILE = DATA_DIR / "productos.csv"


def init_local_files():
    DATA_DIR.mkdir(exist_ok=True)

    if not TXT_FILE.exists():
        TXT_FILE.write_text("", encoding="utf-8")

    if not JSON_FILE.exists():
        JSON_FILE.write_text("[]", encoding="utf-8")

    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id_producto", "nombre", "categoria", "precio", "stock"])


def normalizar_producto(producto):
    return {
        "id_producto": int(producto["id_producto"]),
        "nombre": str(producto["nombre"]),
        "categoria": str(producto["categoria"]),
        "precio": float(producto["precio"]) if isinstance(producto["precio"], Decimal) else float(producto["precio"]),
        "stock": int(producto["stock"])
    }


def sincronizar_persistencia(productos_mysql):
    init_local_files()

    productos_normalizados = [normalizar_producto(p) for p in productos_mysql]

    # TXT
    with TXT_FILE.open("w", encoding="utf-8") as file:
        if productos_normalizados:
            for producto in productos_normalizados:
                file.write(
                    f"ID: {producto['id_producto']} | "
                    f"Nombre: {producto['nombre']} | "
                    f"Categoría: {producto['categoria']} | "
                    f"Precio: {producto['precio']} | "
                    f"Stock: {producto['stock']}\n"
                )
        else:
            file.write("No existen productos registrados.\n")

    # JSON
    with JSON_FILE.open("w", encoding="utf-8") as file:
        json.dump(productos_normalizados, file, ensure_ascii=False, indent=4)

    # CSV
    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id_producto", "nombre", "categoria", "precio", "stock"])

        for producto in productos_normalizados:
            writer.writerow([
                producto["id_producto"],
                producto["nombre"],
                producto["categoria"],
                producto["precio"],
                producto["stock"]
            ])

    # SQLite
    ProductoSQLite.query.delete()

    for producto in productos_normalizados:
        producto_sqlite = ProductoSQLite(
            id_producto=producto["id_producto"],
            nombre=producto["nombre"],
            categoria=producto["categoria"],
            precio=producto["precio"],
            stock=producto["stock"]
        )
        db.session.add(producto_sqlite)

    db.session.commit()


def leer_txt():
    init_local_files()
    contenido = TXT_FILE.read_text(encoding="utf-8").strip()
    return contenido.splitlines() if contenido else []


def leer_json():
    init_local_files()
    with JSON_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def leer_csv():
    init_local_files()
    datos = []

    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for fila in reader:
            datos.append(fila)

    return datos


def leer_sqlite():
    productos = ProductoSQLite.query.order_by(ProductoSQLite.id_producto.desc()).all()
    return [producto.to_dict() for producto in productos]