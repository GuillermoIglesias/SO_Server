# LINKS INFORMACION
# https://shakeelosmani.wordpress.com/2015/04/13/python-3-socket-programming-example/ 
# http://www.binarytides.com/python-socket-server-code-example/

import socket
import game
from _thread import *

# IP Server y puerto
host = "127.0.0.1"
port = 5035


# Funcion para manejar conecciones por threads.
def ClientThread(conn,addr):
	# Enviar mensaje al cliente conectado
	msg_conn_true = "+ Conectado al servidor existosamente\n"
	conn.send(msg_conn_true.encode())

	game.Welcome(conn,addr)

	# Loop login/register
	while True:
		log_op = conn.recv(1024).decode()
		
		if log_op == 'ingresar':
			game.Login(conn,addr)
			break
		
		elif log_op == 'registrar':
			game.Register(conn,addr)
			break
		
		elif log_op == 'salir':
			game.Logout(conn,addr)
			return

		else:
			conn.send("+ Opcion invalida, intenta nuevamente".encode())

	# Loop infinito para escuchar al cliente continuamente 
	while True:
		# Recibir mensaje del cliente
		data = conn.recv(1024).decode()
		#if not data:
		#	break

        # Imprime en consola servidor mensaje recibido        
		print ("Recibido desde " + str(addr) + " : " + str(data))
            
        # Procesa mensaje recibido             
		data = str(data).upper()         
		print ("sending: " + str(data))

		# Envia mensaje procesado al cliente
		conn.send(data.encode())
             
    # Termina loop         
	conn.close()

def Main():

    # Se crea el socket INET de tipo STREAM, luego se bindea al host y puerto
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mySocket.bind((host,port))

   	# Comenzar escuchando socket
	mySocket.listen(5)
	print ("Servidor funcionando")

    # Mantener conexion con el cliente
	while True:
    	# Espera para aceptar una conexion
		conn, addr = mySocket.accept()
		print ("Se ha conectado: " + str(addr))

        # Iniciar un nuevo thread
		start_new_thread(ClientThread,(conn,addr))

    # Cierra socket para finalizar    
	mySocket.close()
   
     
if __name__ == '__main__':
	Main()

