#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

try:
	from ..cliente.suscriptor import Suscriptor
except ValueError:
	from cliente.suscriptor import Suscriptor

import threading
import time

class CreadorDeSuscriptor(threading.Thread):
	def __init__(self, group = None, target = None, name = None,
				args = (), kwargs = None, temas = [], *,
				daemon = None):
		super().__init__(
			group = group, target = target, daemon = daemon, name = name,
			args = args, kwargs = kwargs
		)
		self.terminar = False

		self.temas_anteriores = temas
		self.temas = temas

	def run(self):
		self.suscriptor = Suscriptor(
			'suscriptor',
			temas = self.temas,
			bucle_infinito = False,
		)

		creador = threading.Thread(
			target = lambda algo: algo.suscriptor.loop_forever(),
			kwargs = {'algo': self}
		)
		creador.setDaemon(True)
		creador.start()

		while True:
			if self.terminar: break
			if self.temas_anteriores != self.temas:
				self.suscriptor.unsubscribe(topic = [tema for tema in self.temas_anteriores])
				self.suscriptor.subscribe(topic = [(tema, self.suscriptor.qos) for tema in self.temas])

				self.suscriptor.temas = self.temas_anteriores = self.temas
				print(f'[\033[1;32mThread_subs\033[0m]\tTemas actualizados: {self.temas}.')

			time.sleep(5)
