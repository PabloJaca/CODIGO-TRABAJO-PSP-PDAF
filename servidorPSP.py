import mysql.connector
from mysql.connector import Error
import socket
import pickle
import threading

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Asegúrate de cambiar esto por tu host
            user='root',       # Cambia 'root' por tu usuario de MySQL
            password='pirineus',       # Pon aquí tu contraseña de MySQL
            database='futibol'  # Asegúrate de usar el nombre correcto de tu base de datos
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def consultar_partidos_por_equipo(nombre_equipo):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estadisticas WHERE equipolocal = %s OR equipovisitante = %s", (nombre_equipo, nombre_equipo,))
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

def consultar_partido_por_id(id_partido):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estadisticas WHERE idpartido = %s", (id_partido,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

def consultar_todos_los_equipos():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT DISTINCT equipolocal FROM estadisticas UNION SELECT DISTINCT equipovisitante FROM estadisticas")
        equipos = cursor.fetchall()
        conexion.close()
        return [equipo[0] for equipo in equipos]

def insertar_nueva_estadistica(idpartido, equipovisitante, equipolocal, resultado, competicion):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO estadisticas (idpartido, equipovisitante, equipolocal, resultado, competicion) VALUES (%s, %s, %s, %s, %s)",
                       (idpartido, equipovisitante, equipolocal, resultado, competicion))
        conexion.commit()
        conexion.close()
        return "Estadística insertada con éxito."

def manejar_cliente(conn, addr):
    print(f"Conectado por {addr}")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            solicitud = pickle.loads(data)
            if solicitud['accion'] == 'consultar_por_equipo':
                respuesta = consultar_partidos_por_equipo(solicitud['nombre_equipo'])
            elif solicitud['accion'] == 'consultar_por_id':
                respuesta = consultar_partido_por_id(solicitud['id_partido'])
            elif solicitud['accion'] == 'consultar_todos_los_equipos':
                respuesta = consultar_todos_los_equipos()
            elif solicitud['accion'] == 'insertar_nueva_estadistica':
                respuesta = insertar_nueva_estadistica(**solicitud['datos'])
            else:
                respuesta = "Acción no reconocida."
            conn.sendall(pickle.dumps(respuesta))
    finally:
        conn.close()
        print(f"Conexión con {addr} cerrada.")

def servidor_programa():
    host = '10.10.10.20'
    port = 65432
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, port))
    servidor_socket.listen()
    print(f"Servidor escuchando en {host}:{port}...")

    while True:
        conn, addr = servidor_socket.accept()
        threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

if __name__ == '__main__':
    servidor_programa()
