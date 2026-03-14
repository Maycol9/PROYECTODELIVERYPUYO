from flask import Flask, render_template, request, redirect, url_for
from database import Inventario

app = Flask(__name__)
mi_inventario = Inventario()

@app.route('/')
def home():
    # Obtenemos los productos de la base de datos
    productos = mi_inventario.obtener_todos()
    return render_template('index.html', productos=productos)

@app.route('/añadir', methods=['POST'])
def añadir():
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio'))
    stock = int(request.form.get('stock'))
    mi_inventario.añadir_producto(nombre, precio, stock)
    return redirect(url_for('home'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    mi_inventario.eliminar_producto(id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)