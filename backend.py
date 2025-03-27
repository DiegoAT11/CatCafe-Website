from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

datos = []
user_info = {}


conn = sqlite3.connect('catcafe.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS items (nombre TEXT)''')

c.execute("SELECT COUNT(*) FROM items")
if c.fetchone()[0] == 0:
    nombres = ['Tiramisu', 'Cheesecakes', 'RolesdeCanela', 'Donas']
    for nombre in nombres:
        c.execute("INSERT INTO items (nombre) VALUES (?)", (nombre,))


c.execute('''CREATE TABLE IF NOT EXISTS credenciales (
                    id INTEGER PRIMARY KEY,
                    email TEXT,
                    password TEXT
                )''')


c.execute("SELECT COUNT(*) FROM credenciales")
if c.fetchone()[0] == 0:
    credenciales_iniciales = [
        ('diegoaguilar@admin.com', 'diego12345'),
        ('rodrigofernando@admin.com', 'rodrigo09876'),
        ('manuelantonio@admin.com', 'manuel13579'),
        ('davidalonso@admin.com', 'david24680'),
        ('joseangel@admin.com', 'jose12457')
    ]
    c.executemany("INSERT INTO credenciales (email, password) VALUES (?, ?)", credenciales_iniciales)


conn.commit()
conn.close()

conn = sqlite3.connect('catcafe.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS precios_productos (
                    id_producto INTEGER PRIMARY KEY,
                    precio REAL
                )''')

cursor.execute("SELECT COUNT(*) FROM precios_productos")
if cursor.fetchone()[0] == 0:
    precios = [(1, 55.0), (2, 35.0), (3, 45.0), (4, 25.0)]
    cursor.executemany("INSERT INTO precios_productos (id_producto, precio) VALUES (?, ?)", precios)



cursor.execute('''CREATE TABLE IF NOT EXISTS adopciones (
                    id_solicitud INTEGER PRIMARY KEY,
                    nombre_gato TEXT,
                    nombre_usuario TEXT,
                    edad_usuario INTEGER,
                    email TEXT,
                    telefono TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS gatos (
                    id_gato INTEGER PRIMARY KEY,
                    nombre_gato TEXT,
                    edad_gato TEXT,
                    pelo TEXT,
                    comportamiento_gato TEXT
                )''')

conn.commit()



@app.route("/login", methods=["POST", "GET"])
def valid_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('catcafe.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM credenciales WHERE email = ? AND password = ?", (email, password))
        credencial = cursor.fetchone()

        conn.close()

        if credencial:
            return 'Acceso válido'
        else:
            return 'Credenciales inválidas'

    elif request.method == "GET":
        conn = sqlite3.connect('catcafe.db')
        c = conn.cursor()

        c.execute("SELECT * FROM credenciales")
        credenciales = c.fetchall()

        conn.close()

        return jsonify(credenciales=credenciales)


@app.route("/adopcion", methods=["POST", "GET"])
def valid_adoption():
    if request.method == "POST":
        nombre_gato = request.form['nombre_gato']
        nombre_usuario = request.form['nombre_usuario']
        edad_usuario = request.form['edad_usuario']
        email = request.form['email']
        telefono = request.form['telefono']

        conn = sqlite3.connect('catcafe.db')
        c = conn.cursor()
        
        c.execute("INSERT INTO adopciones (nombre_gato, nombre_usuario, edad_usuario, email, telefono) VALUES (?, ?, ?, ?, ?)",
                  (nombre_gato, nombre_usuario, edad_usuario, email, telefono))
        
        conn.commit()
        conn.close()
        
        return "ok"

    elif request.method == "GET":
        
        conn = sqlite3.connect('catcafe.db')
        c = conn.cursor()

        c.execute("SELECT * FROM adopciones")
        adopciones = c.fetchall()

        conn.close()

        return jsonify(adopciones=adopciones)


@app.route('/datos')
def index():
    conn = sqlite3.connect('mi_base_de_datos.db')
    c = conn.cursor()

    c.execute("SELECT nombre FROM items")
    rows = c.fetchall()
    items = [row[0] for row in rows]

    conn.close()

    return jsonify(items=items)


@app.route('/precios', methods=['GET'])
def obtener_precios():
    conn = sqlite3.connect('catcafe.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id_producto, precio FROM precios_productos")
    precios = cursor.fetchall()

    conn.close()

    return jsonify(precios)


@app.route('/gatos', methods=['GET'])
def obtener_gatos():
    conn = sqlite3.connect('catcafe.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id_gato, nombre_gato, edad_gato, pelo, comportamiento_gato FROM gatos")
    gatos = cursor.fetchall()

    conn.close()

    return jsonify(gatos)


@app.route('/modificar_gatos', methods=['GET', 'POST'])
def modificar_gatos():
    if request.method == 'POST':
        id_gato = request.form.get('modificar_gato')
        nueva_edad = request.form.get('nueva_edad')
        nuevo_pelo = request.form.get('nuevo_pelo')
        nuevo_comportamiento = request.form.get('nuevo_comportamiento')

        conn = sqlite3.connect('catcafe.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE gatos SET edad_gato = ?, pelo = ?, comportamiento_gato = ? WHERE id_gato = ?", 
                       (nueva_edad, nuevo_pelo, nuevo_comportamiento, id_gato))

        conn.commit()
        conn.close()

        return "Datos del gato modificados con éxito."

    elif request.method == 'GET':
        conn = sqlite3.connect('catcafe.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id_gato, nombre_gato FROM gatos")
        gatos = cursor.fetchall()

        conn.close()

        return render_template('gatos_admin.html', gatos=gatos)

    return "Error: Método no permitido."


@app.route('/borrar', methods=['GET', 'POST'])
def borrar_agregar():
    if request.method == 'POST':
        items_to_delete = request.form.getlist('borrar_item')
        items_to_add = request.form.getlist('agregar_item')

        conn = sqlite3.connect('mi_base_de_datos.db')
        c = conn.cursor()

        for item in items_to_delete:
            c.execute("DELETE FROM items WHERE nombre=?", (item,))

        for item in items_to_add:
            c.execute("INSERT INTO items (nombre) VALUES (?)", (item,))

        conn.commit()
        conn.close()

        return "Ok"

    else:
        conn = sqlite3.connect('mi_base_de_datos.db')
        c = conn.cursor()

        c.execute("SELECT nombre FROM items")
        rows = c.fetchall()
        items = [row[0] for row in rows]

        conn.close()

        return render_template('borrar.html', items=items)

if __name__ == '__main__':
    app.run()


