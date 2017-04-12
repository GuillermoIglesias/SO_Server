import psycopg2
import re
import random

hostname = "localhost"
username = "postgres"
password = "jazzbebe123"
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
			cur.execute("SELECT pass,id FROM player WHERE username = %s;",(username,))
			result 	   = cur.fetchall()
			passResult = result[0][0]
			idResult = result[0][1]

			# Validar resultado consulta
			if passResult == password:
				print("Usuario: " + username + " validado desde: " + str(addr))
				msgSuccess = "+ Ingresado correctamente"
				conn.send(msgSuccess.encode())
				return idResult

		except:
			# Error al ingresar usuario, preguntar nuevamente
			msgError = "+ Error: username y/o password incorrectos\n+ Ingresa Username: "
			conn.send(msgError.encode())
		

	return idResult

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

	return id_usr

def Battle(id_usr):
	msgInicio=("+ Inicia batalla:")

	# Elige monstruo
	monster = random.randint(1,5)
	cur.execute("SELECT name,maxhp,atk FROM Monster where id = %s;",(monster,))
	datos_monster = cur.fetchall()
	name_monster = datos_monster[0][0]
	hp_monster = datos_monster[0][1]	
	atk_monster = datos_monster[0][2]

	# Datos usuario
	cur.execute("SELECT hp,atk FROM stats where id= %s",(id_usr,))
	datos_usuario = cur.fetchall()
	hp_usr = datos_usuario[0][0]
	atk_usr = datos_usuario[0][1]

	conexion.commit()

	conn.send(name_monster.encode())
	conn.send(hp_monster.encode())
	conn.send(atk_monster.encode())

	conn.send(hp_usr.encode())
	conn.send(atk_usr.encode())

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

	# Matriz con datos de ganados 'g' o perdedor 'p'
	mtr_atk = [['0','p','g'],['g','0','p'],['p','p','0']]
	res_vid_usr = int(hp_usr)
	res_vid_mon = int(hp_monster)

	# Insertan los datos en las tablas CurrentMonster y CurrentUser
	cur.execute("INSERT INTO currentmonseter(id,current_hp) values(%s,%s);",(monster,res_vid_mon))
	cur.execute("INSERT INTO currentuser(id,current_hp) values(%s,%s);",(id_usr,res_vid_usr))

	while True:
		
		try:
			# Pide ataque
			msgBattle = ("+ Selecciona un ataque: \n"
				   " [fuego]\n"
				   " [agua]\n"
				   " [planta]\n")

			conn.send(msgBattle.encode())


			# Recibir ataque
			atk =  str(conn.recv(1024).decode())
			
			atk_monster = random.randint(0,2)
			# 0 agua, 1 fuego, 2 planta

			# Verifica nuemro de ataque, dentro de la matriz
			if atk == 'fuego':
				atk_usr = int(1)
			elif atk == 'agua':
				atk_usr = int(0)
			else:
				atk_usr = int(2)

			# Busca dentro de la matriz
			battle = mtr_atk[atk_monster][atk_usr]


			# Si el usuario pierde
			if battle == 'p':
				# Se resta su vida
				res_vid_usr = res_vid_usr - int(atk_monster)
		
				# Mientras su vida sea mayor a cero
				if res_vid_usr > 0:
					msg1=("+ Has perdido " + str(atk_monster)+ "de hp\n+ Te queda "
					+str(res_vid_usr)+"de hp\n+ A " +str(name_monster) 
					+" le queda "+ (res_vid_mon)+" de hp \n")

					# Se actualizan los datos de CurrentUser
					cur.execute("UPDATE currentuser set current_hp=%s where id=%s; ",(res_vid_usr,id_usr))
					conn.send(mg1.encode())

				# Pierde
				else:
					msgLose=("+ Perdiste\n")
					cur.execute("UPDATE currentuser set current_hp=%s where id=%s; ",(res_vid_usr,id_usr))
					conn.send(msgLose.encode())

			# Se el usuario gana
			elif battle == 'g':
				# Resta vida a monstruo
				res_vid_mon = res_vid_mon - int(atk_usr)

				# Mientras la vida de monstruo sea mayor a cero
				if res_vid_mon > 0:
					msg2=("+ " + str(name_monster) + " ha perdido " + str(atk_usr)+ 
					"de hp\n+ Te queda "+str(res_vid_usr)+"de hp\n+ A " 
					+str(name_monster) +" le queda "+ (res_vid_mon)+" de hp \n")

					# Se actualiza los datos de CurrentMonster
					cur.execute("UPDATE currentmonster set current_hp=%s where id=%s; ",(res_vid_mon,monster))
					conn.send(mg2.encode())

				# Gana
				else:
					msgWin = ("+ Ganaste!\n")
					cur.execute("UPDATE currentmonster set current_hp=%s where id=%s; ",(res_vid_mon,monster))
					conn.send(msgWin.encode())
						
			# Si hacen el mismo ataque
			else:
				msg3=("+ Ataques bloqueados\n")
				conn.send(mg3.encode())


		except:
			# Mensaje Error
			msgError = "+ Error: Al ingresar\n"
			conn.send(msgError.encode())

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
