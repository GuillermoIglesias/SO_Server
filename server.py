# LINKS INFORMACION
# https://shakeelosmani.wordpress.com/2015/04/13/python-3-socket-programming-example/ 
# http://www.binarytides.com/python-socket-server-code-example/

import socket
import sys
from _thread import *

# Funcion para manejar conecciones por threads.
def ClientThread(conn,addr):
	# Enviar mensaje al cliente conectado
	#msg_conn_true = "Conectado al server existosamente"
	#conn.send(msg_conn_true.enconde())

	# Loop infinito para escuchar al cliente continuamente 
	while True:
		# Recibir mensaje del cliente
		data = conn.recv(1024).decode()
		if not data:
			break

        # Imprime en consola servidor mensaje recibido        
		print ("from " + str(addr) + " : " + str(data))
            
        # Procesa mensaje recibido             
		data = str(data).upper()         
		print ("sending: " + str(data))

		# Envia mensaje procesado al cliente
		conn.send(data.encode())
             
    # Termina loop         
	conn.close()

def Main():
	# IP Server y puerto
	host = "127.0.0.1"
	port = 5004
     
    # Se crea el socket INET de tipo STREAM, luego se bindea al host y puerto
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mySocket.bind((host,port))

   	# Comenzar escuchando socket
	mySocket.listen(5)

    # Mantener conexion con el cliente
	while True:
    	# Espera para aceptar una conexion
		conn, addr = mySocket.accept()
		print ("Connection from: " + str(addr))

        # Iniciar un nuevo thread
		start_new_thread(ClientThread,(conn,addr))

    # Cierra socket para finalizar    
	mySocket.close()
   
     
if __name__ == '__main__':
	Main()

