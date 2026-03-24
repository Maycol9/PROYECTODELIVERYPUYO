from fpdf import FPDF


def texto_seguro(valor):
    return str(valor).encode("latin-1", "replace").decode("latin-1")


def generar_pdf_productos(productos, ruta_archivo):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título principal
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "Reporte de Productos - DeliverPuyo", 0, 1, "C")

    # Subtítulo
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        190,
        8,
        texto_seguro("Resumen del catálogo de productos registrados en la plataforma DeliverPuyo."),
        0,
        1,
        "C"
    )

    pdf.ln(5)

    # Encabezados de tabla
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(15, 10, "ID", 1, 0, "C")
    pdf.cell(60, 10, "Nombre", 1, 0, "C")
    pdf.cell(40, 10, "Categoria", 1, 0, "C")
    pdf.cell(35, 10, "Precio", 1, 0, "C")
    pdf.cell(25, 10, "Stock", 1, 1, "C")

    # Contenido
    pdf.set_font("Helvetica", "", 10)

    if productos:
        for producto in productos:
            pdf.cell(15, 10, texto_seguro(producto["id_producto"]), 1)
            pdf.cell(60, 10, texto_seguro(producto["nombre"])[:30], 1)
            pdf.cell(40, 10, texto_seguro(producto["categoria"])[:20], 1)
            pdf.cell(35, 10, f"${float(producto['precio']):.2f}", 1)
            pdf.cell(25, 10, texto_seguro(producto["stock"]), 1)
            pdf.ln()
    else:
        pdf.cell(
            175,
            10,
            texto_seguro("No existen productos registrados en DeliverPuyo."),
            1,
            1,
            "C"
        )

    pdf.ln(8)

    # Pie informativo
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(
        0,
        6,
        texto_seguro(
            "Documento generado automáticamente por DeliverPuyo para control y consulta "
            "del catálogo de productos del sistema."
        )
    )

    pdf.output(ruta_archivo)