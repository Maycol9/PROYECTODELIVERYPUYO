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
