class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio, categoria):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio
        self.__categoria = categoria

    def get_id_producto(self):
        return self.__id_producto

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    def get_categoria(self):
        return self.__categoria

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def set_precio(self, precio):
        self.__precio = precio

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def to_dict(self):
        return {
            "id": self.__id_producto,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio,
            "categoria": self.__categoria
        }

    def __str__(self):
        return (
            f"ID: {self.__id_producto} | "
            f"Nombre: {self.__nombre} | "
            f"Cantidad: {self.__cantidad} | "
            f"Precio: ${self.__precio:.2f} | "
            f"Categoría: {self.__categoria}"
        )