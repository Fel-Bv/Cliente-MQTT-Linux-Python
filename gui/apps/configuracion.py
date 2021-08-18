#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from cambiar_configuracion import guardar_configuracion
from encriptar.encriptar import e
from gui.campo_texto import CampoContraseña
from gui.campo_texto import CampoTexto
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QHBoxLayout
from qtpy.QtWidgets import QLineEdit
from gui.checkbox import CheckBox
from gui.ventana import Ventana
from gui.boton import Boton
from gui.texto import Texto
from qtpy import QtWidgets
import sys

class ConfiguracionGUI(Ventana):
	def __init__(self, parent = None, layout = QVBoxLayout):
		super().__init__(parent = parent, layout = layout, titulo = 'Configuración')

		titulo = Texto('Configuración')

		self.agregar_widget(titulo)

		self.formulario_broker = {
			'texto': Texto('Broker:'),
			'ip': CampoTexto('Dirección IP o dominio'),
			'puerto': CampoTexto('Puerto', '1883'),
		}
		self.formulario_credenciales = {
			'existen': CheckBox('¿Autorización de acceso?'),
			'usuario': CampoTexto(placeholder = 'Nombre de usuario'),
			'contraseña': CampoContraseña(placeholder = 'Contraseña'),
		}
		self.formulario_credenciales['existen'].stateChanged.connect(self.credenciales_cambio_estado)
		self.formulario_credenciales['usuario'].setEnabled(False)
		self.formulario_credenciales['contraseña'].setEnabled(False)
		self.formulario_credenciales['contraseña'].setEchoMode(CampoTexto.Password)

		formulario_broker_layout = QHBoxLayout()
		for widget in self.formulario_broker: formulario_broker_layout.addWidget(self.formulario_broker[widget])

		formulario_credenciales_layout = QHBoxLayout()
		for widget in self.formulario_credenciales: formulario_credenciales_layout.addWidget(self.formulario_credenciales[widget])

		self.agregar_layout(formulario_broker_layout)
		self.agregar_layout(formulario_credenciales_layout)

		self.boton_guardar = Boton('Guardar')
		self.boton_guardar.clicked.connect(self.guardar)

		self.agregar_widget(self.boton_guardar)
		
		# for campo in filter(lambda widget: isinstance(widget, QLineEdit), [*self.formulario_broker.values(), *self.formulario_credenciales.values()]):
		# 	print(campo)

	def __call__(self):
		self.resize(500, 150)

		qRect = self.frameGeometry()
		centro = QtWidgets.QDesktopWidget().availableGeometry().center()
		qRect.moveCenter(centro)

		self.move(qRect.topLeft())

		super().__call__()

	@property
	def hay_credenciales(self):
		return self.formulario_credenciales['existen'].isChecked()

	def credenciales_cambio_estado(self):
		self.formulario_credenciales['usuario'].setEnabled(self.hay_credenciales)
		self.formulario_credenciales['contraseña'].setEnabled(self.hay_credenciales)

	def guardar(self):
		contraseña = e(self.formulario_credenciales['contraseña'].text())
		usuario = self.formulario_credenciales['usuario'].text()
		puerto = self.formulario_broker['puerto'].text()
		ip = self.formulario_broker['ip'].text()
		configuracion = ''

		if not self.validar(ip, puerto, usuario, contraseña): return

		if self.hay_credenciales:
			configuracion += (
				'credenciales  = {'
				f'\n\t"usuario": "{usuario}",\n'
				f'\t"contraseña": {contraseña}\n'
				'}\n'
			)
		else: configuracion += 'credenciales  = {}\n'
		if puerto and ip:
			configuracion += (
				f'broker        = "{ip}"\n'
				f'puerto        = {puerto}\n'
			)
		else: return

		guardar_configuracion(configuracion)
		# if self.parent(): self.parent().close()
		# else: self.close()

		if self.parent(): self.parent().mensaje.setText('Reinicia la aplicación')
		
		self.agregar_widget(Texto('Configuración guardada'))

	def validar(self, ip, puerto, usuario, contraseña):
		try:
			# Validar que exista la dirección IP
			if not ip: raise ValueError
			print('[\033[1;32mValidando\033[0m]\tDirección IP válida.')

			# Validar el tipo de dato del puerto
			int(puerto)
			print('[\033[1;32mValidando\033[0m]\tPuerto válido.')

			# Validar tipo de dato del usuario y contraseña
			if self.hay_credenciales:
				if usuario and contraseña:
					assert type(usuario) in [str, bytes] and type(contraseña) in [str, bytes], "Tipo de dato inválido."
					print('[\033[1;32mValidando\033[0m]\tCredenciales válidas.')
				else: return False
		except ValueError or AssertionError: return False

		return True

def main():
	try:
		app = QApplication(sys.argv)
		ConfiguracionGUI()()
		sys.exit(app.exec_())
	except RuntimeError: ConfiguracionGUI()()