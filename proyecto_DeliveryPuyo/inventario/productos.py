# Requisito: Clase Producto con atributos básicos
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"Producto: {self.nombre} - Precio: {self.precio}"

    def to_dict(self):
        return {"nombre": self.nombre, "precio": self.precio}