#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from .cliente import Cliente

class Suscriptor(Cliente):
	def __init__(self, ID = '', limpiar_sesion = True, tema = 'mqtt/#', temas:list = [],
			qos = 2, bucle_infinito = True, mostrar_notificacion_al_recibir_mensaje = True):
		Cliente.__init__(
			self, {'id': ID, 'limpiar sesion': limpiar_sesion},
			mostrar_notificacion_al_recibir_mensaje = mostrar_notificacion_al_recibir_mensaje
		)

		self.tema = tema
		self.qos = qos
		self.temas = temas
		self.resultado_conexion = self.conectar()

		if bucle_infinito: self.loop_forever()

	def on_connect(self, *args, **kwargs):
		super().on_connect(*args, **kwargs)

		if self.tema not in self.temas:
			self.subscribe(topic = self.tema, qos = self.qos)

		if self.temas:
			self.subscribe(topic = [(tema, self.qos) for tema in self.temas])

	def on_subscribe(self, datos_de_usuario, *args):
		suscriptor = datos_de_usuario._client_id.decode(encoding = 'UTF-8', errors = 'strict')
		for tema in self.temas:
			print(f'[\033[1;32mSuscripción\033[0m]\t«{suscriptor}» se ha suscrito a "{tema}".')
