import psycopg2
import re

hostname = "localhost"
username = "postgres"
password = "dragon"
database = "SocketDungeon"

conexion = psycopg2.connect(host=hostname,user=username,password=password,dbname=database)
cur      = conexion.cursor()

def Welcome(conn,addr):
	msgWelcome = ("+-------------------------------+\n"
	"|  Bienvenido a Socket Dungeon  |\n"
	"|                               |\n"
	"| Elige una opcion:             |\n"
	"| [ingresar]  : Iniciar sesion  |\n"
	"| [registrar] : Nuevo usuario   |\n"
	"| [salir]     : Salir del juego |\n"
	"+-------------------------------+\n")

	conn.send(msgWelcome.encode())
	return

def Login(conn,addr):
	validate = False

	while validate == False:
		msgUser = "+ Ingresa Username: "
		conn.send(msgUser.encode())

		username = conn.recv(1024).decode()

		msgPass = "+ Ingresa Password: "
		conn.send(msgPass.encode())

		password = conn.recv(1024).decode()
		# chequear la base #

		# if chequear == True:
		# 	validate == True
		#	break
		# msgError = "+ Username y/o Password incorrectos"

	return

def Logout(conn,addr):
	conn.send("+ Desconectado".encode())
	conn.close()
	return

def Register(conn,addr):

	# Pedir username
	msgRegUser = "+ Ingresa Username: "
	conn.send(msgRegUser.encode())

	# Recibir username
	username = str(conn.recv(1024).decode())

	# Pedir email
	msgRegMail = "+ Ingresa Email: "
	conn.send(msgRegMail.encode())

	# Validar direccion email (formato)
	while True:
		mail = str(conn.recv(1024).decode())
		# Validacion email
		if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',mail.lower()):
			break
		else:
			# Solicitar email nuevamente en caso de error
			msgRegMail = "+ Error: correo invalido\n+ Ingresa Email: "
			conn.send(msgRegMail.encode())
	
	# Pedir password
	msgRegPass = "+ Ingresa Password: "
	conn.send(msgRegPass.encode())

	# Recibir password
	password = str(conn.recv(1024).decode())	

	# Se inserta nuevo usuario a la base de datos
	cur.execute("INSERT INTO Player(username,mail,pass) VALUES (%s,%s,%s);",(username,mail,password))

	# Mensaje de exito
	print("Creado usuario " + username + " desde: " + str(addr))
	msgSuccess = "+ Usuario creado exitosamente"
	conn.send(msgSuccess.encode())

	return

def Battle(conn,addr):
	return



# Solo para pruebas #
def Main():
	msg1 = ("+-------------------------------+\n"
	"|  Bienvenido a Socket Dungeon  |\n"
	"|                               |\n"
	"| Elige una opcion:             |\n"
	"| 1.- Ingresar                  |\n"
	"| 2.- Nuevo Usuario             |\n"
	"| 3.- Salir                     |\n"
	"+-------------------------------+")

	print (msg1)

	cur.execute("select * from monster")
	resultado = cur.fetchall()
	conexion.commit()
	nombre=resultado
	print (nombre)

	print ("+ Error: correo invalido\n+ Ingresa Email: ")


if __name__ == '__main__':
	Main()


