class RegistroForm:
    def __init__(self, form_data):
        self.nombre = form_data.get("nombre", "").strip()
        self.email = form_data.get("email", "").strip()
        self.password = form_data.get("password", "").strip()
        self.confirmar_password = form_data.get("confirmar_password", "").strip()
        self.errores = []

    def validar(self):
        self.errores = []

        if not self.nombre:
            self.errores.append("El nombre es obligatorio.")

        if not self.email:
            self.errores.append("El correo es obligatorio.")
        elif "@" not in self.email or "." not in self.email:
            self.errores.append("El correo no tiene un formato válido.")

        if not self.password:
            self.errores.append("La contraseña es obligatoria.")
        elif len(self.password) < 6:
            self.errores.append("La contraseña debe tener al menos 6 caracteres.")

        if self.password != self.confirmar_password:
            self.errores.append("Las contraseñas no coinciden.")

        return len(self.errores) == 0