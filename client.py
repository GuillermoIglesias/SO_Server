#!/usr/bin/python3

import socket

# IP Server y puerto
host = "127.0.0.1"
port = 5054

def Main():
    while True:

        print ('Conectando al servidor...')

        # Welcome 
        while True:
            try:
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mySocket.connect((host,port))
                data = mySocket.recv(1024).decode()
                if data:               
                    print (data)
                
                msgWelcome = mySocket.recv(1024).decode()
                if msgWelcome:               
                    print (msgWelcome)
                
                break        
            
            except:
                continue

        # Menu login/register
        while True:
            op_input = input('>>> ')

            try:
                mySocket.send(op_input.encode())
                data = mySocket.recv(1024).decode()               
                print (data)
                
                if op_input == 'salir':
                    mySocket.close()
                    return

                if data == '+ Usuario creado exitosamente' or data == '+ Ingresado correctamente':
                    break

            
            except:
                print ('Servidor desconectado')
                break

        # Imprime monstruo inicial
        #monsterSprite = mySocket.recv(1024).decode()
        #print(monsterSprite)
        
        while True:
	
            startBattle = mySocket.recv(1024).decode()
            print(startBattle)
               
            message = input('>> ')


            try:
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()      
                print (data)

                if data == '\n+ Ganaste ^.^!\n' or data == '\n+ Perdiste x.x\n':
                	while True:
                		question = mySocket.recv(1024).decode()
                		print (question)	
                		message = input('> ')
                		mySocket.send(message.encode())
                		if message == 'Y' or message == 'y' or message == 'yes':
                			break
                		elif message == 'N' or message == 'n' or message =='no':
                			mySocket.close()
                			return

           	#if message == 'salir':
			#mySocket.close()
            #	return
            
            except:
                print ('Servidor desconectado')
                break

            
    
 
if __name__ == '__main__':
    Main()
