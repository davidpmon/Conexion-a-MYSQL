import requests  # Importa la biblioteca requests para hacer peticiones HTTP

def obtener_usuarios():
    response = requests.get('http://localhost:5000/usuarios')
    if response.status_code == 200:
        usuarios = response.json()
        print("\nUsuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios")

def buscar_id(id_usuario):
    url = f'http://localhost:5000/usuarios/{id_usuario}'
    response = requests.get(url)
    if response.status_code == 200:
        usuario = response.json()
        print(f"\nUsuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    elif response.status_code == 404:
        print("Usuario no encontrado")
    else:
        print("Error al buscar usuario")

def registrar_usuario(nombre):
    # Realiza una petición POST al servidor para registrar un nuevo usuario
    response = requests.post('http://localhost:5000/usuarios', json={'nombre': nombre})
    if response.status_code == 201:  # Si el usuario se registró correctamente (código 201)
        print("Usuario registrado:", response.json())
    else:
        print("Error al registrar el usuario")  # Muestra un mensaje de error si la solicitud falla


if __name__ == '__main__':
    obtener_usuarios()  # Ejecuta la función al iniciar el script
    registrar_usuario("Nuevo Usuario")  # Registra un nuevo usuario
    print("1. Obtener todos los usuarios")
    print("2. Buscar usuario por ID")
    opcion = input("Selecciona una opción: ")

    if opcion == '1':
        obtener_usuarios()
    elif opcion == '2':
        try:
            id_usuario = int(input("Ingresa el ID del usuario: "))
            buscar_id(id_usuario)
        except ValueError:
            print("Por favor, ingresa un ID válido.")
    else:
        print("Opción no válida.")

 