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

	# Pedir username
	msgUser = "+ Ingresa Username: "
	conn.send(msgUser.encode())

	while True:
		# Recibir username
		username = str(conn.recv(1024).decode())

		# Pedir password
		msgPass = "+ Ingresa Password: "
		conn.send(msgPass.encode())

		# Recibir password
		password = str(conn.recv(1024).decode())
		
		try:
			# Realizar consulta a la base de datos
			cur.execute("SELECT pass FROM player WHERE username = %s;",(username,))
			result 	   = cur.fetchall()
			passResult = result[0][0]

			# Validar resultado consulta
			if passResult == password:
				print("Usuario: " + username + " validado desde: " + str(addr))
				msgSuccess = "+ Ingresado correctamente"
				conn.send(msgSuccess.encode())
				break

		except:
			# Error al ingresar usuario, preguntar nuevamente
			msgError = "+ Error: username y/o password incorrectos\n+ Ingresa Username: "
			conn.send(msgError.encode())
		

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
	cur.execute("INSERT INTO player(username,mail,pass) VALUES(%s,%s,%s);",(username,mail,password))
	# Se ingresa su stats
	cur.execute("SELECT id from player where username= %s;",(username,))
	id_username = cur.fetchall()
	id_usr = id_username[0][0]
	cur.execute("INSERT INTO stats(id,hp,atk,level) VALUES(%s,500,20,1);",(id_usr,))
	conexion.commit()

	# Mensaje de exito
	print("Creado usuario " + username + " desde: " + str(addr))
	msgSuccess = "+ Usuario creado exitosamente"
	conn.send(msgSuccess.encode())

	return

def Battle(conn,addr):
	# Elige monstruo
	monster = random.randint(1,5)
	cur.execute("SELECT name,maxhp,atk FROM Monster where id = %s;",(monster,))
	datos_monster = cur.fetchall()
	name_monster = datos_monster[0][0]
	hp_monster = datos_monster[0][1]	
	atk_monster = datos_monster[0][2]

	conn.send(name_monster.encode())
	conn.send(hp_monster.encode())
	conn.send(atk_monster.encode())

	msgMonster = ("      D  D     \n"
	"      D  D     \n"
	"     DDDDDD    \n"
	"    DD-DD-DD   \n"
	"    DDDDDDDD   \n"
	"     DD--DD    \n"
	"  D   DDDD   D \n"
	"   D DDDDDD D  \n"
	"    DDDDDDDD   \n"
	"   DDDDDDDDDD  \n"
	"   DDDDDDDDDD  \n"
	"    DDDDDDDD   \n"
	"     DDDDDD    \n"
	"     DD  DD    \n"
	"     DD  DD    \n"
	"     DDD DDD   \n")

	conn.send(msgMonster.encode())
	while True:
		msgBattle = "+ ATACA !!!!"
		conn.send(msgBattle.encode())
		

	return



# Solo para pruebas #
def Main():
	
	try:
		cur.execute("select pass from player where username = 'coco'")
		resultado = cur.fetchall()
		conexion.commit()
		nombre=resultado[0][0]
		print (nombre)
	except:
		print("Error")

	print ("      D  D     \n"
	"      D  D     \n"
	"     DDDDDD    \n"
	"    DD-DD-DD   \n"
	"    DDDDDDDD   \n"
	"     DD--DD    \n"
	"  D   DDDD   D \n"
	"   D DDDDDD D  \n"
	"    DDDDDDDD   \n"
	"   DDDDDDDDDD  \n"
	"   DDDDDDDDDD  \n"
	"    DDDDDDDD   \n"
	"     DDDDDD    \n"
	"     DD  DD    \n"
	"     DD  DD    \n"
	"     DDD DDD   \n")

if __name__ == '__main__':
	Main()


