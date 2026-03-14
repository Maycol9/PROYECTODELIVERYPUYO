from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Renderiza el archivo index.html
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    # Renderiza el archivo nosotros.html
    return render_template('nosotros.html')

@app.route('/pedido/<int:id_pedido>')
def consultar_pedido(id_pedido):
    # Aquí puedes pasar variables a la plantilla
    return render_template('index.html', pedido_id=id_pedido)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)