#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QIcon
from pathlib import Path
import sys

class Ventana(QWidget):
	def __init__(self, parent = None, layout = QVBoxLayout, titulo = 'Ventana :)'):
		super().__init__(parent = parent)

		self.layout = layout()
		self.titulo = titulo

		self.ruta_icono = Path('.', 'imgs', 'icono.png')
		self.setWindowIcon(QIcon(str(self.ruta_icono)))

		self.setStyleSheet(
			open('./gui/qss/ventana.css', 'r').read()
		)

	def __call__(self):
		self.setWindowTitle(self.titulo)
		self.setLayout(self.layout)
		self.show()

	def agregar_widget(self, widget):
		self.layout.addWidget(widget)

	def agregar_layout(self, layout):
		self.layout.addLayout(layout)

	def keyPressEvent(self, evento):
		if evento.key() == 16777216:
			sys.exit(0)