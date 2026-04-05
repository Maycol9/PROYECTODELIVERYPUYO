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
