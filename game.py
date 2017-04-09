import psycopg2

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

	msgRegUser = "+ Ingresa Username: "
	conn.send(msgRegUser.encode())


	msgRegMail = "+ Ingresa Email: "
	conn.send(msgRegMail.encode())

	msgRegPass = "+ Ingresa Password: "
	conn.send(msgRegPass.encode())

	msgSuccess = "+ Usuario creado exitosamente +"
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


if __name__ == '__main__':
	Main()