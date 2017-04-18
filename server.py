#!/usr/bin/python3

import socket
import game
import random
from _thread import *

# IP Server y puerto
host = "127.0.0.1"
port = 5072

# Funcion para manejar conexiones por threads.
def ClientThread(conn,addr):
	# Iniciar conexion con cliente	
	id_user = game.Welcome(conn,addr)

	if id_user == '-1':

		# Loop login/register
		while True:
			try:
				log_op = conn.recv(1024).decode()
				
				if log_op == 'ingresar':
					id_user = game.Login(conn,addr)
					break
				
				elif log_op == 'registrar':
					id_user = game.Register(conn,addr)
					break
				
				elif log_op == 'salir':
					game.Logout(conn,addr)
					return

				else:
					conn.send("+ Opcion invalida, intenta nuevamente\n".encode())
			except:
				conn.close()
				return

	#monster = str(random.randint(1,5))	
	monster = "3"
	print(id_user)
	# Loop infinito para escuchar al cliente continuamente
	while True:
		try:
			game.Battle(id_user,monster,conn)
		except:
			conn.close()
			return

		if game.Continue(conn):
			continue
		else:
			game.Logout(conn,addr)
			return

    # Termina loop         
	conn.close()
	return

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
