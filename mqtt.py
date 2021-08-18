#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from encriptar.encriptar import *
from config.config import *
from dependencias import *
from encriptar import encriptar
import sys

try:
	from gui.menus.principal import BarraMenuPrincipal
	from gui.apps.suscriptor import SuscriptorGUI
	from encriptar.encriptar import *
	from gui.apps.publicar import PublicadorGUI
	from gui.campo_texto import CampoTexto
	from qtpy.QtWidgets import QApplication
	from qtpy.QtWidgets import QMainWindow
	from qtpy.QtWidgets import QVBoxLayout
	from gui.apps.login import LoginGUI
	from gui.ventana import Ventana
	from gui.texto import Texto
	from qtpy import QtWidgets
except ImportError:
	try:
		print('[\033[1;31mERROR\033[00m]\t\tLas dependencias no estan instaladas.')
		instalar = input('\t\t¿Deseas instalarlas? [s/n]: ')
	except:
		print('\nSaliendo...\n')

		from sys import exit
		exit(0)

	if instalar in ['y', 'yes', 's', 'si', 't', 'true', 'v']: instalar_dependencias()

encriptar.__name__ = e('horse playing football')

principal = None

class Aplicacion(Ventana):
	def __init__(self, layout = QVBoxLayout, parent = None) -> None:
		super().__init__(layout = layout, titulo = 'Conexión a Broker MQTT', parent = parent)

		self.mostrar_login() if credenciales else self.__iniciar()

	def __call__(self) -> None:
		self.setMinimumSize(580, 420)

		qRect = self.frameGeometry()
		centro = QtWidgets.QDesktopWidget().availableGeometry().center()
		qRect.moveCenter(centro)

		self.move(qRect.topLeft())

		super().__call__()

	def __iniciar(self) -> None:
		try: del self.login
		except AttributeError: pass

		self.layout.setSpacing(5)

		self.suscriptor = SuscriptorGUI()
		self.publicador = PublicadorGUI()

		self.resultado_conexion = ''
		while not self.resultado_conexion:
			try:
				self.resultado_conexion = self.suscriptor.creador_de_subs.suscriptor.resultado_conexion
			except AttributeError:
				from time import sleep
				sleep(1)

		self.mensaje = Texto(self.resultado_conexion)

		self.agregar_widget(BarraMenuPrincipal(self))
		self.agregar_widget(self.mensaje)

		if not 'conectado a' in self.resultado_conexion.lower(): return

		self.agregar_widget(self.suscriptor)
		self.agregar_widget(self.publicador)

		self.publicador.mensaje.focusInEvent = self.focus_en_mensaje

		self.suscriptor()
		self.publicador()

		self.suscriptor.temas.setFocus()

	def mostrar_login(self) -> None:
		# Muestra la GUI
		self.login = LoginGUI()

		self.agregar_widget(self.login)
		self.login()

		# Verifica las credenciales
		def iniciar_sesion():
			if self.login.login():
				print('[\033[1;32mLogin\033[0m]\t\tSe ha inciado sesión')
				self.login.setVisible(False)

				self.layout.removeWidget(self.login)
				self.login.deleteLater()

				self.__iniciar()
				return

			self.login.limpiar_campos()
			self.login.formulario['usuario'].setFocus()

		self.login.formulario['enviar'].clicked.connect(iniciar_sesion)

	def focus_en_mensaje(self, *args) -> None:
		self.suscriptor.cambiar_temas(evento_externo = True)
		self.publicador.cambiar_tema(evento_externo = True)
		CampoTexto.focusInEvent(self.publicador.mensaje, *args)

	def reiniciar(self):
		self.suscriptor.creador_de_subs.terminar = True

		eliminar_ventana_principal()
		iniciar_ventana_principal()

def eliminar_ventana_principal() -> None:
	global principal

	principal.close()
	principal = None
	print(principal)

def iniciar_ventana_principal():
	global principal

	principal = Aplicacion()
	principal()

def main() -> None:
	global principal

	app = QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(True)

	iniciar_ventana_principal()

	sys.exit(app.exec_())

if __name__ == '__main__':
	try: main()
	except KeyboardInterrupt:
		sys.stdout.write('\nSaliendo...\n')
		sys.exit(0)
