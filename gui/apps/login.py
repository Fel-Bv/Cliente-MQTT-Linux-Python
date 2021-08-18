#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from encriptar.encriptar import *
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QVBoxLayout
from config.config import *
from gui.campo_texto import CampoContraseña
from gui.campo_texto import CampoTexto
from gui.ventana import Ventana
from gui.texto import Texto
from gui.boton import Boton
from qtpy import QtWidgets
import sys

class LoginGUI(Ventana):
	def __init__(self, parent = None, layout = QVBoxLayout):
		super().__init__(parent = parent, layout = layout, titulo = 'Login')

		titulo = Texto('Inicia sesión')

		self.formulario = {
			'usuario': CampoTexto(placeholder = 'Usuario'),
			'contraseña': CampoContraseña(placeholder = 'Contraseña'),
			'enviar': Boton('Iniciar sesión'),
		}
		self.formulario['contraseña'].setEchoMode(QtWidgets.QLineEdit.Password)

		formulario = QVBoxLayout()
		formulario.addWidget(self.formulario['usuario'])
		formulario.addWidget(self.formulario['contraseña'])
		formulario.addWidget(self.formulario['enviar'])

		self.agregar_widget(titulo)
		self.agregar_layout(formulario)

	def __call__(self):
		self.resize(400, 100)

		qRect = self.frameGeometry()
		centro = QtWidgets.QDesktopWidget().availableGeometry().center()
		qRect.moveCenter(centro)

		self.move(qRect.topLeft())

		super().__call__()

	def login(self):
		usuario = self.formulario['usuario'].text()
		contraseña = self.formulario['contraseña'].text()

		self.limpiar_campos()

		# print(credenciales['contraseña'].decode())

		if not usuario or not contraseña: return
		if	usuario == credenciales['usuario'] and \
			contraseña == d(credenciales['contraseña']).decode(): return True

		return False

	def limpiar_campos(self):
		self.formulario['usuario'].setText('')
		self.formulario['contraseña'].setText('')

	def keyPressEvent(self, evento):
		super().keyPressEvent(evento)

		if evento.key() == 16777220: self.formulario['enviar'].click()

def main():
	app = QApplication(sys.argv)
	app.setQuitOnLastWindowClosed()

	principal = LoginGUI()
	principal()

	sys.exit(principal.exec_())

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nSaliendo...\n')
		sys.exit(0)