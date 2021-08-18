#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont

class Texto(QLabel):
	def __init__(self, texto):
		QLabel.__init__(self)

		self.setFont(QFont('Arial', 24, QFont.Bold))
		self.setAlignment(Qt.AlignCenter)
		self.setStyleSheet(
			open(
				'./gui/qss/texto.css', 'r'
			).read()
		)

		self.setText(texto)