from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from Conexion.conexion import obtener_configuracion

app = Flask(__name__)

# Configuración de MySQL
conf = obtener_configuracion()
app.config['MYSQL_HOST'] = conf['host']
app.config['MYSQL_USER'] = conf['user']
app.config['MYSQL_PASSWORD'] = conf['password']
app.config['MYSQL_DB'] = conf['database']

mysql = MySQL(app)

# --- REQUISITO 3: Creación de Tablas (Ejecutar una vez en MySQL) ---
# CREATE TABLE usuarios (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), mail VARCHAR(100), password VARCHAR(100));
# CREATE TABLE pedidos (id_pedido INT AUTO_INCREMENT PRIMARY KEY, cliente VARCHAR(100), descripcion TEXT, estado VARCHAR(50));

@app.route('/')
def index():
    return render_template('index.html')

# --- REQUISITO 4: Consultas y CRUD ---

@app.route('/usuarios')
def listar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=data)

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form['nombre']
    mail = request.form['mail']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)", (nombre, mail, password))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_usuarios'))

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_usuarios'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)