class Producto:
    def __init__(self, id_producto=None, nombre="", stock=0, precio=0.0, categoria=""):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__stock = stock
        self.__precio = precio
        self.__categoria = categoria

    def get_id_producto(self):
        return self.__id_producto

    def get_nombre(self):
        return self.__nombre

    def get_stock(self):
        return self.__stock

    def get_precio(self):
        return self.__precio

    def get_categoria(self):
        return self.__categoria

    def set_id_producto(self, id_producto):
        self.__id_producto = id_producto

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_stock(self, stock):
        self.__stock = stock

    def set_precio(self, precio):
        self.__precio = precio

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def to_dict(self):
        return {
            "id_producto": self.__id_producto,
            "nombre": self.__nombre,
            "stock": self.__stock,
            "precio": self.__precio,
            "categoria": self.__categoria
        }

    def __str__(self):
        return (
            f"ID: {self.__id_producto} | "
            f"Nombre: {self.__nombre} | "
            f"Stock: {self.__stock} | "
            f"Precio: ${float(self.__precio):.2f} | "
            f"Categoría: {self.__categoria}"
        )