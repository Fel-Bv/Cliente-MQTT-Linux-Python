#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def verificar_libreria_notify():
	from subprocess import check_output as ejecutar, PIPE

	try: ejecutar('notify -v', shell = True, stdout = PIPE)
	except:
		print('[\033[1;34mInfo\033[0m]\t\t"notify-send" no está instalado. ¿Deseas instalarlo? [s/n]: ', end='')
		instalar = input('').strip().lower()
		if instalar in ['y', 'yes', 's', 'si', 't', 'true', 'v']:
			from platform import dist, system
			import os

			if 'windows' in system().lower():
				print('\t\tVisita la página: https://github.com/vaskovsky/notify-send')
				return

			print('[\033[1;34mInfo\033[0m]\t\tInstalando «libnotify»...')

			dist = dist()[0].lower()

			if dist in ['debian', 'ubuntu', 'deepin']: os.system('sudo apt install libnotify-bin -y')
			elif dist in ['kali', 'raspbian']: os.system('sudo apt-get install libnotify-bin -y')
			elif dist in ['fedora', 'centos']: os.system('sudo dnf install libnotify -y')
			elif dist == 'alpine': os.system('sudo apk add libnotify -y')
			elif dist == 'arch': os.system('sudo pacman -S libnotify -y')
			elif dist == 'mac': os.system('brew install libnotify -y')
			else:
				print('[\033[1;31mERROR\033[0m]\t\tDistribución desconocida.')
				print('\t\t\tIntenta instalar «libnotify» con el administrador de paquetes de tu distribución.')

			del os, dist, PIPE
		del ejecutar

	print()

def verificar_libreria_mosquitto():
	from subprocess import check_output as ejecutar, PIPE

	try: ejecutar('mosquitto -v', shell = True, stdout = PIPE)
	except:
		print('[\033[1;34mInfo\033[0m]\t\tLa libreria "mosquitto" no está instalada. ¿Deseas instalarla? [s/n]: ', end='')
		instalar = input('').strip().lower()
		if instalar in ['y', 'yes', 's', 'si', 't', 'true', 'v']:
			from platform import dist, system
			import os

			if 'windows' in system().lower():
				print('\t\tVisita la página: https://mosquitto.org/download/')
				return

			print('[\033[1;34mInfo\033[0m]\t\tInstalando «mosquitto»...')

			dist = dist()[0].lower()

			if dist in ['debian', 'ubuntu', 'deepin']: os.system('sudo apt install mosquitto -y')
			elif dist in ['kali', 'raspbian']: os.system('sudo apt-get install mosquitto -y')
			elif dist in ['fedora', 'centos']: os.system('sudo dnf install mosquitto -y')
			elif dist == 'alpine': os.system('sudo apk add mosquitto -y')
			elif dist == 'arch': os.system('sudo pacman -S mosquitto -y')
			elif dist == 'mac': os.system('brew install mosquitto -y')
			else:
				print('[\033[1;31mERROR\033[0m]\t\tDistribución desconocida.')
				print('\t\t\tIntenta instalar "mosquitto" con el administrador de paquetes de tu distribución.')

			del os, dist, PIPE
		del ejecutar

	print()

def instalar_dependencias():
	# verificar_libreria_mosquitto()
	verificar_libreria_notify()

	from os import system

	dependencias = open('requirements.pip', 'r').read().strip().split('\n')

	for paquete in dependencias:
		print(f'[\033[1;34mInfo\033[0m]\t\tInstalando «{paquete}»...')
		system(f'pip3 install {paquete} || pip install {paquete}')
		print()

if __name__ == '__main__':
	try: instalar_dependencias()
	except KeyboardInterrupt: print('\nSaliendo...\n')
	except Exception as error: print(f'[\033[1;31mERROR\033[0m]\t\t{error}') 