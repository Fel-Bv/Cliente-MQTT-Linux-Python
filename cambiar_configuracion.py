#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from encriptar.encriptar import *
from getpass import getpass
from shutil import get_terminal_size
from config import config
from time import sleep
import sys
import os

credenciales_a_configurar = config.credenciales
puerto_a_configurar = config.puerto
broker = config.broker
configuracion = ''

def guardar_configuracion_mosquitto():
	global puerto_a_configurar, credenciales_a_configurar, broker

	configuracion = f'''# listener «puerto» «ip»
# mitla listener 8080 10.0.10.58
# casa  listener 8080 192.168.100.5
listener {puerto_a_configurar} {broker}

'''
	if not credenciales_a_configurar: configuracion += '''
# allow_anonymous false
# password_file /etc/mosquitto/passwd

'''
	else: configuracion += '''
allow_anonymous false
password_file /etc/mosquitto/passwd

'''

	with open('/etc/mosquitto/conf.d/default.conf', 'w') as archivo:
		archivo.seek(0)
		archivo.write(configuracion)

	os.system('sudo systemctl restart mosquitto')

def guardar_configuracion(config = None):
	if not config: global configuracion
	else: configuracion = config
	if not configuracion: return
	if not 'credenciales' in configuracion:
		configuracion = 'credenciales  = {'
		if config.credenciales:
			configuracion += f'\n\t"usuario": \'{config.credenciales["usuario"]}\',\n'
			configuracion += f'\t"contraseña": {config.credenciales["contraseña"]},\n'
		configuracion += '}\n'
	if not 'broker' in configuracion: configuracion += f'broker        = "{config.broker}"\n'
	if not 'puerto' in configuracion: configuracion += f'puerto        = {config.puerto}\n'

	# print(configuracion)

	with open('./config/config.py', 'w') as archivo:
		archivo.seek(0)
		archivo.write(configuracion)

def pedir_contraseña():
	contraseña = getpass(prompt = '[credenciales]\t Ingrese la contraseña: ')

	return e(contraseña)

def pedir_usuario():
	texto = '[credenciales]\t Ingrese el nombre de usuario'

	if config.credenciales:
		try:
			texto += f' ({config.credenciales["usuario"]})' if config.credenciales['usuario'] else ''
		except KeyError:
			pass

	texto += ': '
	usuario = input(texto)

	return usuario if usuario else config.credenciales['usuario']

def pedir_ip():
	texto = '[broker]\t Ingrese la dirección IP del broker'
	texto += f' ({config.broker})' if config.broker else ''
	texto += ': '
	broker = input(texto)

	return broker if broker else config.broker

def pedir_puerto():
	texto = '[broker]\t Ingrese el puerto del broker'
	texto += f' ({config.puerto})' if config.puerto else ''
	texto += ': '
	puerto = input(texto)

	return puerto if puerto else config.puerto

def hay_credenciales():
	limpiar_consola()

	return input(
		'¿Hay credenciales? [s/n]: '
	).lower() == 's'

def configurar_credenciales():
	global credenciales_a_configurar
	global configuracion

	if hay_credenciales():
		limpiar_consola()

		usuario = pedir_usuario()
		contraseña = pedir_contraseña()

		credenciales_a_configurar = {'usuario': usuario, 'contraseña': contraseña}

		configuracion += 'credenciales  = {\n'
		configuracion += f'\t"usuario": \'{usuario}\',\n'
		configuracion += f'\t"contraseña": {contraseña},\n'
		configuracion += '}\n'
	else:
		credenciales_a_configurar = {}
		configuracion += 'credenciales  = {}\n'

	limpiar_consola()
	print('Guardando configuración de credenciales...')
	sleep(.5)
	limpiar_consola()

def configurar_broker():
	global puerto_a_configurar, broker
	global configuracion

	limpiar_consola()

	ip = pedir_ip()
	puerto = pedir_puerto()

	broker = ip
	puerto_a_configurar = puerto

	configuracion += f'broker        = \'{ip}\'\n'
	configuracion += f'puerto        = {puerto}\n'

	limpiar_consola()
	print('Guardando configuración del broker...')
	sleep(.5)
	limpiar_consola()

def limpiar_consola(imprimir_titulo_ = True):
	os.system('clear')
	if imprimir_titulo_: imprimir_titulo()

def imprimir_titulo():
	tamaño_terminal = get_terminal_size().columns
	titulo = ' Configuracion '

	print(titulo.center(tamaño_terminal, '-'))


def main():
	from encriptar import encriptar

	encriptar.__name__ = e('horse playing football')



	global configuracion

	limpiar_consola()

	if input('¿Desea configurar las credenciales? [s/n]: ').lower() == 's': configurar_credenciales()
	if input('¿Desea configurar las opciones del broker? [s/n]: ').lower() == 's': configurar_broker()

	limpiar_consola()

	if configuracion:
		print('Guardando información...')
		sleep(.5)
		guardar_configuracion()
		if input('¿Guardar la información en el servidor mosquitto local? [s/n]: ').lower() == 's': guardar_configuracion_mosquitto()

	limpiar_consola(imprimir_titulo_ = False)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nSaliendo...\n')
		sys.exit(0)
