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
