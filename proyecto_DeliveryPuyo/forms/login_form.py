class LoginForm:
    def __init__(self, form_data):
        self.email = (form_data.get("email", "") or "").strip().lower()
        self.password = (form_data.get("password", "") or "").strip()
        self.errores = []

    def validar(self):
        self.errores = []

        if not self.email:
            self.errores.append("El correo electrónico es obligatorio.")
        if not self.password:
            self.errores.append("La contraseña es obligatoria.")

        return len(self.errores) == 0
