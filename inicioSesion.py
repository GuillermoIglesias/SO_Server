# LINKS INFORMACION
# https://shakeelosmani.wordpress.com/2015/04/13/python-3-socket-programming-example/ 
# http://www.binarytides.com/python-socket-server-code-example/

import socket
import sys
from _thread import *

hostname = "localhost"
username = "postgres"
password = "jazzbebe123"
database = "prueba"

import psycopg2




# Funcion para manejar conecciones por threads.
def ClientThread(conn):
	# Enviar mensaje al cliente conectado
	#msg_conn_true = "Conectado al server existosamente"
	#conn.send(msg_conn_true.enconde())

	conexion= psycopg2.connect(host=hostname, user=username, password=password, dbname=database )

	cur=conexion.cursor()


	# Loop infinito para escuchar al cliente continuamente 
	while True:
		# Recibir mensaje del cliente
		data = conn.recv(1024).decode()
		if not data:
			break

        # Imprime en consola servidor mensaje recibido        
		print ("from connected  user: " + str(data))
		name = str(data)
		cur.execute("select nombre from usuarios where nombre= %s;", (name,))
		resultado = cur.fetchall()
		conexion.commit()

		nombre=resultado[0]

            
        # Procesa mensaje recibido             
		data = str(data).upper()         
		print ("sending: " + str(nombre[0]))

		# Envia mensaje procesado al cliente
		conn.send(data.encode())
             
    # Termina loop         
	conn.close()

	cur.close()
	conexion.close()

def Main():
	# IP Server y puerto
	host = "127.0.0.1"
	port = 5003
     
    # Se crea el socket, luego se bindea al host y puerto
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mySocket.bind((host,port))

   	# Comenzar escuchando socket
	mySocket.listen(2)

    # Mantener conexion con el cliente
	while True:
    	# Espera para aceptar una conexion
		conn, addr = mySocket.accept()
		print ("Connection from: " + str(addr))

        # Iniciar un nuevo thread
		start_new_thread(ClientThread,(conn,))

    # Cierra socket para finalizar    
	mySocket.close()
   
     
if __name__ == '__main__':
	Main()
