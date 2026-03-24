class ProductoForm:
    def __init__(self, form_data):
        self.nombre = form_data.get("nombre", "").strip()
        self.categoria = form_data.get("categoria", "").strip()
        self.precio = form_data.get("precio", "").strip()
        self.stock = form_data.get("stock", "").strip()
        self.errores = []

    def validar(self):
        self.errores = []

        if not self.nombre:
            self.errores.append("El nombre es obligatorio.")

        if not self.categoria:
            self.errores.append("La categoría es obligatoria.")

        try:
            precio_val = float(self.precio)
            if precio_val <= 0:
                self.errores.append("El precio debe ser mayor a 0.")
        except ValueError:
            self.errores.append("El precio debe ser numérico.")

        try:
            stock_val = int(self.stock)
            if stock_val < 0:
                self.errores.append("El stock no puede ser negativo.")
        except ValueError:
            self.errores.append("El stock debe ser un número entero.")

        return len(self.errores) == 0