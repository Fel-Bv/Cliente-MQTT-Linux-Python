#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from .cliente import Cliente
import sys

class Publicador(Cliente):
	def __init__(self, ID = '', limpiar_sesion = False):
		Cliente.__init__(self, {'id': ID, 'limpiar sesion': limpiar_sesion})

	def publicar(self, mensaje = 'Publicación', tema = 'mqtt', qos = 0):
		resultado_conexion: str = self.conectar()
		if not 'conectado a' in resultado_conexion.lower(): return resultado_conexion

		try: self.publish(topic = tema, payload = mensaje, qos = qos, retain = False)
		except ValueError as e:
			print(f'[\033[1;31mERROR\033[0m]\t\t{e}')
			sys.exit(1)

		print(f'[\033[1;32mExito\033[0m]\t\tMensaje publicado en «{tema}»: {mensaje}.')
		self.disconnect()

		return resultado_conexion
