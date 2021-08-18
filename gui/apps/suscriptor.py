#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from hilos.creador_de_subs import CreadorDeSuscriptor
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QVBoxLayout
from gui.campo_texto import CampoTexto
from gui.ventana import Ventana
from gui.texto import Texto
from gui.boton import Boton
from qtpy import QtWidgets
import sys

class SuscriptorGUI(Ventana):
	def __init__(self, parent = None, layout = QVBoxLayout):
		super().__init__(parent = parent, layout = layout, titulo = 'Suscriptor')

		self.creador_de_subs = CreadorDeSuscriptor()
		self.creador_de_subs.setDaemon(True)
		self.creador_de_subs.start()

		titulo = QVBoxLayout()
		titulo.addWidget(Texto('Suscriptor'))

		self.temas = CampoTexto('Temas a suscribirse separados por coma. Ejemplo: "tema/mqtt, mqtt/#"')
		self.cambiar_temas_btn = Boton('Suscribir')
		self.cambiar_temas_btn.clicked.connect(self.cambiar_temas)
		formulario = QVBoxLayout()
		formulario.addWidget(self.temas)
		formulario.addWidget(self.cambiar_temas_btn)

		self.agregar_layout(titulo)
		self.agregar_layout(formulario)

	def __call__(self):
		self.resize(400, 100)

		qRect = self.frameGeometry()
		centro = QtWidgets.QDesktopWidget().availableGeometry().center()
		qRect.moveCenter(centro)

		self.move(qRect.topLeft())

		super().__call__()

	def cambiar_temas(self, evento_externo = False):
		if not self.temas.text(): return

		nuevos_temas = self.temas.text().split(', ')

		if nuevos_temas == self.creador_de_subs.temas: return

		self.creador_de_subs.temas = nuevos_temas

		print(
			f'[\033[1;32mSuscriptor\033[0m]\tSe han cambiado los temas: {self.creador_de_subs.temas}.'
		)
		if not evento_externo: self.temas.setFocus()

	def keyPressEvent(self, evento):
		super().keyPressEvent(evento)

		if evento.key() == 16777220: self.cambiar_temas_btn.click()

def main():
	app = QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(True)

	principal = SuscriptorGUI()
	principal()

	sys.exit(app.exec_())

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.stdout.write('\nSaliendo...\n')
		sys.exit(0)