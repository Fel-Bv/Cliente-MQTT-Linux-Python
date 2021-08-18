#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from encriptar.encriptar import *
from paho.mqtt.client import Client
from config.config import *
import sys
import os

from encriptar import encriptar

encriptar.__name__ = e('horse playing football')

exec(open('./config/config.py', 'r').read())


def salir_forzosamente():
	print('\nSaliendo...\n')
	try:
		sys._exit(1)
	except AttributeError:
			import signal

			os.kill(os.getpid(), signal.SIGINT)
			sys.exit(1)
			# os.system('killall python3.7 || echo ""')

class Cliente(Client):
	def __init__(self, cliente:dict, mostrar_notificacion_al_recibir_mensaje = True):
		Client.__init__(self, client_id = cliente['id'], clean_session = cliente['limpiar sesion'])

		if credenciales:
			self.username_pw_set(
				credenciales['usuario'],
				d(credenciales['contraseña']).decode(encoding = 'UTF-8', errors = 'strict')
			)

		self.mostrar_notificacion_al_recibir_mensaje = mostrar_notificacion_al_recibir_mensaje

	def conectar(self):
		try: self.connect(host = broker, port = puerto)

		# Error en el tipo de dato de algun parametro de configuración en ./cliente/cliente.py:
		except ValueError:
			print(
				'[\033[1;31mERROR\033[0m]\t\tLa configuración en "./cliente/cliente.py" es inválida.'
			)

			return f'Configuración de conexión "{broker}:{puerto}" inválida'

		# Error al conectar al broker y puerto indicados:
		except ConnectionRefusedError:
			print(
				'[\033[1;31mERROR\033[0m]\t\tNo me he podido conectar, verifica la direccion y el puerto del broker en config/config.py.'
			)

			return f'Conexión a "{broker}:{puerto}" rechazada'

		# Error de conexión a internet u algún otro error del sistema operativo:
		except OSError:
			print('[\033[1;31mERROR\033[0m]\t\tNo me he podido conectar.')

			return f'"{broker}:{puerto}". Verifica tu conexión a internet'

		# En caso de no tener ningun error, devuelve la siguiente cadena:
		return f'Conectado a {broker}:{puerto}'

	def on_connect(self, cliente, *args, **kwargs):
		cliente_id = self._client_id.decode(encoding = 'UTF-8', errors = 'strict')
		print(f'[\033[1;32mConexión\033[0m]\t«{cliente_id}» se ha conectado.')

	def on_message(self, cliente, userdata, mensaje):
		texto = mensaje.payload.decode(encoding = 'UTF-8', errors = 'strict')
		print(f'[\033[1;32mMensaje\033[0m]\tSe ha recibido un mensaje: Tema «{mensaje.topic}»: {texto}.')
		if self.mostrar_notificacion_al_recibir_mensaje:
			os.system(
				f'notify-send -t 3000 -a "Servidor MQTT" "Se ha recibido un mensaje" \'Tema «{mensaje.topic}»: {texto}.\''
			)
