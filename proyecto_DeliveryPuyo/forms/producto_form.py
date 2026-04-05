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
