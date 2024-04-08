import socket
import pickle

def mostrar_menu():
    print("1. Consultar partidos por nombre de equipo")
    print("2. Consultar partido por ID")
    print("3. Consultar todos los equipos")
    print("4. Insertar nueva estadística")
    print("5. Salir")

def cliente_programa():
    host = '10.10.10.20'
    port = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            mostrar_menu()
            opcion = input("Seleccione una opción: ")
            solicitud = {}
            if opcion == '1':
                nombre_equipo = input("Ingrese el nombre del equipo: ")
                solicitud = {'accion': 'consultar_por_equipo', 'nombre_equipo': nombre_equipo}
            elif opcion == '2':
                id_partido = input("Ingrese el ID del partido: ")
                solicitud = {'accion': 'consultar_por_id', 'id_partido': id_partido}
            elif opcion == '3':
                solicitud = {'accion': 'consultar_todos_los_equipos'}
            elif opcion == '4':
                datos = {
                    'idpartido': input("ID del partido: "),
                    'equipovisitante': input("Equipo visitante: "),
                    'equipolocal': input("Equipo local: "),
                    'resultado': input("Resultado: "),
                    'competicion': input("Competición: ")
                }
                solicitud = {'accion': 'insertar_nueva_estadistica', 'datos': datos}
            elif opcion == '5':
                break
            else:
                print("Opción no válida")
                continue
            s.sendall(pickle.dumps(solicitud))
            respuesta = s.recv(1024)
            print("Respuesta:", pickle.loads(respuesta))

if __name__ == '__main__':
    cliente_programa()
