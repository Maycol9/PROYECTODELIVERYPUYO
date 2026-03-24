class Pedido:
    def __init__(self, id_pedido=None, id_usuario=None, fecha=None, total=0.0, estado="pendiente"):
        self.id_pedido = id_pedido
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.total = total
        self.estado = estado