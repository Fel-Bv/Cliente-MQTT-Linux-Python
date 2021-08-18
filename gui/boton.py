#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from qtpy.QtWidgets import QPushButton
from qtpy.QtCore import Qt
from qtpy.QtGui import QPalette
from qtpy.QtGui import QColor
from qtpy import QtGui
import sys

class Boton(QPushButton):
	def __init__(self, texto, tipo = 'primario'):
		QPushButton.__init__(self, text = texto)

		self.establecer_hoja_de_estilos(tipo)

	def establecer_hoja_de_estilos(self, tipo):
		self.setAutoFillBackground(True)
		if tipo == 'primario':
			self.setStyleSheet(
				open(
					'./gui/qss/boton.css', 'r'
				).read()
			)
		else:
			self.setStyleSheet(
				open(
					'./gui/qss/boton-secundario.css', 'r'
				).read()
			)

	def keyPressEvent(self, evento):
		if evento.key() == 16777220:
			self.click()

		elif evento.key() == 16777216:
			sys.exit(0)