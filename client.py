#!/usr/bin/python3

import socket

# IP Server y puerto
host = "127.0.0.1"
port = 5072

def Main():
	# ID Usuario no logueado/registrado
	validate = '-1'

	while True:

		print ('Conectando al servidor...')

        # Welcome 
		while True:
			try:
				mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				mySocket.connect((host,port))
				
				success = mySocket.recv(1024).decode()            
				print (success)

				mySocket.send(validate.encode())
				
				msgWelcome = mySocket.recv(1024).decode()           
				print (msgWelcome)
				
				break        
			except:
				continue

		print(":"+validate)

		if validate == '-1':
	        # Menu login/register
			while True:
				op_input = input('-> ')

				try:
					mySocket.send(op_input.encode())
				except:
					print('Servidor desconectado')

				try:
					data = mySocket.recv(1024).decode()           
					print (data)             
					if op_input == 'salir':
						mySocket.close()
						return
					if data[:18] == '+ Usuario validado':
						validate = data[20:]
						break      
				except:
					print ('Servidor desconectado')
					break

		print("::"+validate)


		while True:

			try:
				startBattle = str(mySocket.recv(1024).decode())
				print(startBattle)
			except:
				print ('Servidor desconectado')
				break

			message = input('>> ')	

			try:
				mySocket.send(message.encode())
			except:
				print ('Servidor desconectado')
				break

			try:
				data = str(mySocket.recv(1024).decode())      
				print (data)
			except:
				print ('Servidor desconectado')
				break

            
    
 
if __name__ == '__main__':
    Main()
