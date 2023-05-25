import sqlite3
from flask import Flask, request

app = Flask(__name__)

def crear_tabla_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def agregar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user is None:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Usuario agregado exitosamente")
    else:
        print("El usuario ya existe en la base de datos")
    
    conn.close()

def verificar_credenciales(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row is not None and row[2] == password:
        return True
    else:
        return False

@app.route("/")
def home():
    return "Bienvenido al sitio web de gestión de claves"

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if verificar_credenciales(username, password):
        return "Inicio de sesión exitoso"
    else:
        return "Credenciales inválidas"

if __name__ == "__main__":
    crear_tabla_usuarios()
    agregar_usuario("catagonzalez", "hola123")
    agregar_usuario("daquiroz", "hola123")
    app.run(port=5000)

