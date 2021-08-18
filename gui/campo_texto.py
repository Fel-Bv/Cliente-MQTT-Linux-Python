#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from qtpy.QtWidgets import QLineEdit
from qtwidgets import PasswordEdit

class CampoTexto(QLineEdit):
	def __init__(self, placeholder = 'Texto', texto_por_defecto = ''):
		QLineEdit.__init__(self)

		self.setPlaceholderText(placeholder)
		self.setStyleSheet(
			open(
				'./gui/qss/campo_texto.css', 'r'
			).read()
		)

		self.setText(texto_por_defecto)

class CampoContraseña(PasswordEdit):
	def __init__(self, mostrar_visibilidad = True, placeholder = 'Texto'):
		super().__init__(show_visibility = mostrar_visibilidad)

		self.setPlaceholderText(placeholder)
		self.setStyleSheet(
			open(
				'./gui/qss/campo_texto.css', 'r'
			).read()
		)