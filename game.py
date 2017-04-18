#!/usr/bin/python3

import psycopg2
import re
import random

# Credenciales de la base de datos
hostname = "localhost"
username = "postgres"
password = "dragon"
database = "SocketDungeon"

# Conexion db
conexion = psycopg2.connect(host=hostname,user=username,password=password,dbname=database)
cur      = conexion.cursor()

def Welcome(conn,addr):
	# Enviar mensaje al cliente conectado
	msg_conn_true = "+ Conectado al servidor existosamente\n"
	conn.send(msg_conn_true.encode())
	
	id_user = conn.recv(1024).decode()

	if id_user == '-1':

		msgWelcome = (" +-------------------------------+\n"
		" |  Bienvenido a Socket Dungeon  |\n"
		" |                               |\n"
		" | Elige una opcion:             |\n"
		" | [ingresar]  : Iniciar sesion  |\n"
		" | [registrar] : Nuevo usuario   |\n"
		" | [salir]     : Salir del juego |\n"
		" +-------------------------------+\n")

		conn.send(msgWelcome.encode())

	else:
		# buscar id usuario
		cur.execute("SELECT username from player where id= %s;",(id_user,))
		id_usr = cur.fetchall()
		id_usrname = id_user[0][0]
		msgWelcome = ("+ Reconectado: " + str(id_usrname))

		conn.send(msgWelcome.encode())
	
	return id_user

def Login(conn,addr):

	# Pedir username
	msgUser = "+ Ingresa Username: "
	idResult = 0
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
				print ("Usuario: " + username + " validado desde: " + str(addr))
				msgSuccess = "+ Usuario validado: " + str(idResult)
				conn.send(msgSuccess.encode())
				return idResult

		except:
			# Error al ingresar usuario, preguntar nuevamente
			msgError = "+ Error: username y/o password incorrectos\n\n+ Ingresa Username: "
			conn.send(msgError.encode())
		
	return idResult

def Logout(conn,addr):
	conn.send("+ Desconectado".encode())
	conn.close()
	return

def MonsterSprite():
	msgMonster = ("\n  <>=======( )    \n"
		" (/\___   /|\ \          ()==========<>_ \n"
		"       \_/ | \ \        //|\   ______/ \)\n"
		"         \_|  \ \      // | \_/ \n"
		"           \|\/| \_   //  /\/ \n"
		"            (00)\ \_//   / \n"
		"           //_/\_\/ /   | \n"
		"          @@/  |=\  \   | \n"
		"               \_=\_ \  | \n"
		"                 \==\ \ |\_ \n"
		"              __(\===\(   )\ \n"
		"             (((~) __(_/    | \n"
		"                  (((~) \   / \n"
		"                 _______/  / \n"
		"                 '--------' \n")
	
	return msgMonster


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
	cur.execute("INSERT INTO currentuser(id,current_hp) values(%s,500);",(id_usr,))
	conexion.commit()

	# Mensaje de exito
	print("Creado usuario " + username + " desde: " + str(addr))
	msgSuccess = "+ Usuario validado: " + str(id_usr)
	conn.send(msgSuccess.encode())

	return id_usr

def Battle(id_usr,monster,conn):

	sprite = True

	while True:

		#msgInicio=("+ Inicia batalla:\n")
		#conn.send(msgInicio.encode())
		atk_usr = int(-1)
		atk_monster_name = ""

		# Elige monstruo
		cur.execute("SELECT name,atk,maxhp FROM Monster where id = %s;",(monster,))
		datos_monster = cur.fetchall()
		name_monster = datos_monster[0][0]
		atk_monster = datos_monster[0][1]
		hp_monster = datos_monster[0][2]

		# Datos usuario
		cur.execute("SELECT atk,hp FROM stats where id= %s;",(str(id_usr),))
		datos_usuario = cur.fetchall()
		atk_user = datos_usuario[0][0]
		hp_user = datos_usuario[0][1]

		# Datos CurrentMonster
		cur.execute("SELECT current_hp FROM currentmonster where id = %s;",(monster,))
		datos_curr_mon = cur.fetchall()
		res_vid_mon = int(datos_curr_mon[0][0])
		print("Vida inicial de montruo: " + str(res_vid_mon))

		# Datos CurrentUser
		cur.execute("SELECT current_hp FROM currentuser where id = %s;",(str(id_usr),))
		datos_curr_usr = cur.fetchall()
		res_vid_usr = int(datos_curr_usr[0][0])
		print("Vida inicial de usuarios: " + str(res_vid_usr))

		

		# Matriz con datos de ganados 'g' o perdedor 'p'
		mtr_atk=[['0','p','g'],['g','0','p'],['p','g','0']]
			
		#        | agua | fuego | planta
		#  agua  |  0   |   p   |    g
		# fuego  |  g   |   0   |    p	
	    # planta |  p   |   p   |    0 

	
		
		try:
			# Pide ataque
			msgBattle = (" +-----------------------+\n"
				   " | Selecciona un ataque: |\n"
				   " | + [1] - [fuego]       |\n"
				   " | + [2] - [agua]        |\n"
				   " | + [3] - [planta]      |\n"
			  	   " +-----------------------+\n")

			# Se ejecuta la primera vez para sprite dragon
			if sprite == True:
				msgBattle = MonsterSprite() + msgBattle
				sprite = False

			conn.send(msgBattle.encode())

			# Recibir ataque
			atk =  conn.recv(1024).decode()
			atkMonster = random.randint(0,2)
			# 0 agua, 1 fuego, 2 planta
			print ("Ataque de usuario: " + str(atk))

			# Verifica numero de ataque, dentro de la matriz
			if atk == 'fuego' or atk == '1':
				atk_usr = int(1)
				battle = mtr_atk[atkMonster][atk_usr]
			elif atk == 'agua' or atk == '2':
				atk_usr = int(0)
				battle = mtr_atk[atkMonster][atk_usr]
			elif atk == 'planta' or atk == '3':
				atk_usr = int(2)
				battle = mtr_atk[atkMonster][atk_usr]
			else:
				battle = '-1'

			if atkMonster == 1:
				atk_monster_name = str('fuego')
			elif atkMonster == 2:
				atk_monster_name = str('planta')
			elif atkMonster == 0:
				atk_monster_name = str('agua')

			print ("Ataque monstruo: " + str(atk_monster_name))

			# Busca dentro de la matriz
			#battle = mtr_atk[atkMonster][atk_usr]
			print("Resultado matriz batalla: " + str(battle))


			# Si el usuario pierde
			if battle == 'p':
				# Se resta su vida
				res_vid_usr = res_vid_usr - int(atk_monster)
				print("Vida restante de jugador: " + str(res_vid_usr))

				# Mientras su vida sea mayor a cero
				if res_vid_usr > 0:
					msg1=("\n+ " + str(name_monster) + " a usado: " + str(atk_monster_name) + "\n+ Has perdido " +
					 str(atk_monster)+ " hp\n"
					+"+ Te queda "
					+str(res_vid_usr)+" hp\n+ A " +str(name_monster) 
					+" le queda "+ str(res_vid_mon)+" hp \n")
					# Se actualizan los datos de CurrentUser
					cur.execute("UPDATE currentuser set current_hp=%s where id=%s; ",(res_vid_usr,str(id_usr)))
					conexion.commit()
					conn.send(msg1.encode())
			
				# Pierde
				else:
					msgLose=("+ Perdiste x.x")
					cur.execute("UPDATE currentmonster set current_hp=%s where id=%s; ",(hp_monster,monster))
					cur.execute("UPDATE currentuser set current_hp=%s where id=%s; ",(hp_user,str(id_usr)))
					conexion.commit()
					conn.send(msgLose.encode())
					return

			# Se el usuario gana
			elif battle == 'g':
			
				# Resta vida a monstruo
				res_vid_mon = res_vid_mon - int(atk_user)
				print("Vida restante de monstruo: " + str(res_vid_mon))
					# Mientras la vida de monstruo sea mayor a cero
				if res_vid_mon > 0:
					msg2=("\n+ " + str(name_monster)+ " a usado: "+ str(atk_monster_name) + "\n+ " + str(name_monster) + " ha perdido " 
					+ str(atk_user)+ 
					" hp\n+ Te queda "+str(res_vid_usr)+" hp\n+ A " 
					+str(name_monster) +" le queda "+ str(res_vid_mon)+" hp \n")
					# Se actualiza los datos de CurrentMonster
					cur.execute("UPDATE currentmonster set current_hp= %s where id= %s; ",(res_vid_mon,monster))
					conexion.commit()
					conn.send(msg2.encode())
		
				

				# Gana
				else:
					msgWin = ("+ Ganaste ^.^!")
					cur.execute("UPDATE currentmonster set current_hp=%s where id=%s; ",(hp_monster,monster))
					cur.execute("UPDATE currentuser set current_hp=%s where id=%s; ",(hp_user,str(id_usr)))
					conexion.commit()
					conn.send(msgWin.encode())
					return
				
			# Si hacen el mismo ataque
			elif battle == '0':
				msg3=("\n+ " + str(name_monster)+ " a usado: "+ str(atk_monster_name) + "\n+ El ataque ha sido bloqueado\n+ Te queda "+str(res_vid_usr)+" hp\n+ A " 
					+str(name_monster) +" le queda "+ str(res_vid_mon)+" hp \n")
				conn.send(msg3.encode())

			else:
				msgError = "\n+ Error: Valor invalido\n"
				conn.send(msgError.encode())
		
		except:
			conn.close()
			return
		
	return

def Continue(conn):
	while True:
		try:	
			# Preguntar si desea continuar
			msgContinue = "\n+ Deseas continuar? [Y/N]"
			conn.send(msgContinue.encode())
			ans = conn.recv(1024).decode()
				
			if ans == 'Y' or ans == 'y' or ans == 'yes':
				msgYes = "\n+ Reiniciando Monstruo +\n"
				conn.send(msgYes.encode())
				return False
			
			elif ans == 'N' or ans == 'n' or ans =='no':
				return True
			
			else:
				msgError = "+ Opcion invalida, intenta nuevamente\n"
				conn.send(msgError.encode())
				continue
		except:
			conn.close()
			return True