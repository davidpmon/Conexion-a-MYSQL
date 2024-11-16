from flask import Flask, jsonify, request, Response, render_template
from functools import wraps
import mysql.connector
from mysql.connector import Error

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión MySQL
def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',  # Cambia por tu usuario de MySQL
            password='1234',  # Cambia por tu contraseña de MySQL
            database='proyecto'  # El nombre de la base de datos creada
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para verificar la autenticación básica
def verificar_autenticacion(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'admin' or auth.password != 'admin':
            return Response('Acceso no autorizado', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return func(*args, **kwargs)
    return decorador

# Ruta para obtener los usuarios desde MySQL
@app.route('/usuarios', methods=['GET'])
@verificar_autenticacion
def obtener_usuarios():
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")  # Consulta para obtener los usuarios
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except Error as e:
        return jsonify({"error": "Error al obtener usuarios: " + str(e)}), 500
    finally:
        conexion.close()

# Ruta para registrar un nuevo usuario en MySQL
@app.route('/usuarios', methods=['POST'])
@verificar_autenticacion
def registrar_usuario():
    try:
        nuevo_usuario = request.get_json()
        nombre = nuevo_usuario.get('nombre')

        # Validaciones del nombre
        if not nombre or len(nombre) < 2 or len(nombre) > 50:
            return jsonify({"error": "El nombre debe tener entre 2 y 50 caracteres"}), 400
        import re
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚ\\s]+$", nombre):
            return jsonify({"error": "El nombre solo puede contener letras y espacios"}), 400

        # Conexión a la base de datos
        conexion = obtener_conexion()
        if conexion is None:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

        # Insertar el nuevo usuario en la base de datos
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        conexion.commit()

        # Obtener el ID del nuevo usuario insertado
        nuevo_id = cursor.lastrowid

        # Crear la respuesta con el nuevo usuario
        nuevo_usuario["id"] = nuevo_id
        return jsonify(nuevo_usuario), 201
    except Exception as e:
        return jsonify({"error": "Error al procesar la solicitud: " + str(e)}), 500
    finally:
        conexion.close()
    
@app.route('/')
@verificar_autenticacion
def index():
    return render_template('index.html')


# Ruta para obtener un usuario específico por ID desde MySQL
@app.route('/usuarios/<int:id>', methods=['GET'])
@verificar_autenticacion
def obtener_usuario(id):
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Error as e:
        return jsonify({"error": "Error al obtener el usuario: " + str(e)}), 500
    finally:
        conexion.close()

# Ruta para eliminar un usuario desde MySQL
@app.route('/usuarios/<int:id>', methods=['DELETE'])
@verificar_autenticacion
def eliminar_usuario(id):
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conexion.commit()

        if cursor.rowcount > 0:
            return jsonify({"mensaje": f"Usuario con ID {id} eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Error as e:
        return jsonify({"error": "Error al eliminar el usuario: " + str(e)}), 500
    finally:
        conexion.close()

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(port=5000)

