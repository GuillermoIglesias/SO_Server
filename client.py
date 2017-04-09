import socket

def SocketReconnect(mySocket):
    try:
        mySocket.connect((host,port))
        return True       
    except:
        return False  
 
def Main():
    host = '127.0.0.1'
    port = 5004           

    exit = False

    while exit == False:

        print ('Conectando al servidor')

        while True:
            try:
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mySocket.connect((host,port))
                print ('Conectado')
                break        
            except:
                continue    
               
        while True:

            message = input(' -> ')

            if message == 'q':
                print ('Desconectado')
                exit = True
                break

            try:
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()
                if data:               
                    print ('Recibido por servidor: ' + data)
            
            except:
                print ('Servidor desconectado')
                break

            
    mySocket.close()
 
if __name__ == '__main__':
    Main()