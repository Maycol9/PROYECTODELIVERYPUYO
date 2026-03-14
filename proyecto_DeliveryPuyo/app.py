from flask import Flask

app = Flask(__name__)

# 1. Ruta Principal: Presentación del Negocio
@app.route('/')
def home():
    return "<h1>Bienvenido a Delivery Puyo</h1><p>Tu comida favorita, directo a la puerta de tu casa en Puyo.</p>"

# 2. Ruta Dinámica: Consulta de Pedidos
# Adaptado a: /pedido/<id_pedido>
@app.route('/pedido/<int:id_pedido>')
def consultar_pedido(id_pedido):
    return f"<h3>Estado del Pedido #{id_pedido}</h3><p>Estimado cliente, su pedido de Delivery Puyo está en camino.</p>"

if __name__ == '__main__':
    app.run(debug=True)