#!/usr/bin/python3

import socket

# IP Server y puerto
host = "127.0.0.1"
port = 5061

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
            op_input = input('-> ')

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

        
        while True:
	
            startBattle = str(mySocket.recv(1024).decode())
            print(startBattle)
               
            message = input('>> ')

            try:
                mySocket.send(message.encode())
                data = str(mySocket.recv(1024).decode())      
                print (data)

            
            except:
                print ('Servidor desconectado')
                break

            
    
 
if __name__ == '__main__':
    Main()
