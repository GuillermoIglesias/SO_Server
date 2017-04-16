# LINKS INFORMACION
# https://shakeelosmani.wordpress.com/2015/04/13/python-3-socket-programming-example/ 
# http://www.binarytides.com/python-socket-server-code-example/

import socket
import game2
import random
from _thread import *

# IP Server y puerto
host = "127.0.0.1"
port = 5040

# Funcion para manejar conecciones por threads.
def ClientThread(conn,addr):
	# Enviar mensaje al cliente conectado
	msg_conn_true = "+ Conectado al servidor existosamente\n"
	conn.send(msg_conn_true.encode())
	result = ""
	game2.Welcome(conn,addr)

	# Loop login/register
	while True:
		log_op = conn.recv(1024).decode()
		
		if log_op == 'ingresar':
			result = game2.Login(conn,addr)
			break
		
		elif log_op == 'registrar':
			result = game2.Register(conn,addr)
			break
		
		elif log_op == 'salir':
			game2.Logout(conn,addr)
			return

		else:
			conn.send("+ Opcion invalida, intenta nuevamente".encode())

	# Loop infinito para escuchar al cliente continuamente 
	monster = str(random.randint(1,5))	
	while True:
		game2.Battle(result,monster,conn)	

		msgContinue = "+ Deseas continuar? [Y/N]"
		while True:
			
			conn.send(msgContinue.encode())
			ans = conn.recv(1024).decode()
			if ans == 'Y' or ans == 'y' or ans == 'yes':
				break
			elif ans == 'N' or ans == 'n' or ans =='no':
				return
			else:
				msgContinue = "+ Opcion invalida, intenta nuevamente\n+ Deseas continuar? [Y/N]"
				continue



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
