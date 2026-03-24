class DetallePedido:
    def __init__(self, id_detalle=None, id_pedido=None, id_producto=None, cantidad=0, subtotal=0.0):
        self.id_detalle = id_detalle
        self.id_pedido = id_pedido
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.subtotal = subtotal