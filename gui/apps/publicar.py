#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from cliente.publicador import Publicador
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QHBoxLayout
from qtpy.QtWidgets import QVBoxLayout
from gui.campo_texto import CampoTexto
from gui.ventana import Ventana
from gui.texto import Texto
from gui.boton import Boton
from qtpy import QtWidgets
import sys

tema = 'mqtt'

class PublicadorGUI(Ventana):
	def __init__(self, parent = None, layout = QVBoxLayout):
		global tema

		super().__init__(parent = parent, layout = layout, titulo = 'Publicar')

		self.publicador = Publicador('publicador')

		formulario_tema = QHBoxLayout()
		self.tema = CampoTexto('Tema')
		self.tema.setText(tema)
		self.cambiar_tema_btn = Boton('Cambiar tema', tipo = 'secundario')
		self.cambiar_tema_btn.clicked.connect(self.cambiar_tema)

		formulario_tema.addWidget(Texto('Tema: '))
		formulario_tema.addWidget(self.tema)
		formulario_tema.addWidget(self.cambiar_tema_btn)

		titulo = QVBoxLayout()
		titulo.addWidget(Texto('Publicador'))

		self.mensaje = CampoTexto('Mensaje')
		self.publicar_btn = Boton('Publicar')
		self.publicar_btn.clicked.connect(self.publicar)

		formulario_mensaje = QVBoxLayout()
		formulario_mensaje.addWidget(self.mensaje)
		formulario_mensaje.addWidget(self.publicar_btn)

		self.agregar_layout(titulo)
		self.agregar_layout(formulario_tema)
		self.agregar_layout(formulario_mensaje)

	def __call__(self):
		self.resize(400, 100)

		qRect = self.frameGeometry()
		centro = QtWidgets.QDesktopWidget().availableGeometry().center()
		qRect.moveCenter(centro)

		self.move(qRect.topLeft())

		super().__call__()

	def cambiar_tema(self, evento_externo = False):
		global tema

		nuevo_tema = self.tema.text()
		if not nuevo_tema:
			self.tema.setText('mqtt')
			return

		if nuevo_tema == tema: return

		tema = nuevo_tema

		print(f'[\033[1;32mPublicador\033[0m]\tSe ha cambiado el tema: {tema}.')
		if not evento_externo: self.mensaje.setFocus()

	def publicar(self):
		global tema

		mensaje = self.mensaje.text()
		if not mensaje: return

		self.publicador.publicar(mensaje = mensaje, tema = tema)
		self.mensaje.setText('')

	def keyPressEvent(self, evento):
		super().keyPressEvent(evento)

		if evento.key() == 16777220: self.publicar_btn.click()

def main():
	app = QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(True)

	principal = PublicadorGUI()
	principal()

	sys.exit(app.exec_())

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.stdout.write('\nSaliendo...\n')
		sys.exit(0)