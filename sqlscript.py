import hashlib
import sqlite3
from flask import Flask, request, g

# Configuración básica de Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite
DATABASE = 'usuarios.db'

# Función para conectar a la base de datos
def conectar_db():
    return sqlite3.connect(DATABASE)

# Función para obtener la conexión a la base de datos
def obtener_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = conectar_db()
    return db

# Creación de tabla para almacenar usuarios y contraseñas si no existe
def crear_tabla_usuarios():
    conn = obtener_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            hash_contrasena TEXT NOT NULL
        )
    ''')
    conn.commit()

# Antes de cada solicitud, asegúrate de tener una conexión a la base de datos
@app.before_request
def antes_de_la_solicitud():
    obtener_db()
    crear_tabla_usuarios()

# Ruta para registrar usuarios y almacenar en la base de datos
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    nombre = request.form.get('nombre')
    contrasena = request.form.get('contrasena')

    # Crear hash de la contraseña
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

    # Insertar usuario en la base de datos
    conn = obtener_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, hash_contrasena) VALUES (?, ?)', (nombre, hash_contrasena))
    conn.commit()

    return 'Usuario registrado correctamente'

# Ruta para validar usuarios
@app.route('/login', methods=['POST'])
def login_usuario():
    nombre = request.form.get('nombre')
    contrasena = request.form.get('contrasena')

    # Obtener hash de la contraseña ingresada
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

    # Consultar si el usuario existe y la contraseña es correcta
    conn = obtener_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre=? AND hash_contrasena=?', (nombre, hash_contrasena))
    usuario = cursor.fetchone()

    if usuario:
        return 'Inicio de sesión exitoso'
    else:
        return 'Nombre de usuario o contraseña incorrectos'

# Manejo de cierre de la conexión a la base de datos después de cada solicitud
@app.teardown_appcontext
def cerrar_conexion(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(port=5800)

