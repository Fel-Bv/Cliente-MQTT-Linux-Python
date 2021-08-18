#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from qtpy.QtWidgets import QMenuBar
from qtpy.QtWidgets import QAction
from qtpy.QtWidgets import QMenu
from qtawesome import icon
import sys

class MenuPrincipal(QMenu):
    def __init__(self, title: str, parent = None) -> None:
        super().__init__(title, parent = parent)
        self.mostrando_menu_configuracion = False
        self.ventana_principal = self.parent().ventana_principal

        self.salir = QAction(
            icon('fa5s.times-circle'),
            '&Salir',
            self
        )
        self.salir.setStatusTip('Salir de la aplicación.')
        self.salir.triggered.connect(lambda: sys.exit(0))
        self.salir.setShortcut('Esc')
        self.addAction(self.salir)

        self.mostrar_configuracion = QAction('Ocultar/Mostrar configuración', self)
        self.mostrar_configuracion.triggered.connect(self.accion_toggle_mostrar_configuracion)
        self.mostrar_configuracion.setStatusTip('Motrar menú de configuración')
        self.mostrar_configuracion.setShortcut('Ctrl+m')
        self.addAction(self.mostrar_configuracion)

        self.reiniciar_ventana = QAction('Reiniciar', self)
        self.reiniciar_ventana.triggered.connect(self.accion_reiniciar_ventana)
        self.reiniciar_ventana.setStatusTip('Reiniciar ventana')
        self.reiniciar_ventana.setShortcut('Ctrl+r')
        self.addAction(self.reiniciar_ventana)

        self.setStyleSheet(
            open(
                './gui/qss/menus.css', 'r'
            ).read()
        )

    def accion_toggle_mostrar_configuracion(self) -> None:
        if not self.mostrando_menu_configuracion:
            from gui.apps.configuracion import ConfiguracionGUI

            configuracion_gui = ConfiguracionGUI()
            self.ventana_principal.widget_configuracion = configuracion_gui
            self.ventana_principal.agregar_widget(configuracion_gui)
            configuracion_gui()
            self.ventana_principal.resize(580, 600)

            self.mostrar_configuracion.setStatusTip('Ocultar menú de configuración')
        else:
            self.ventana_principal.widget_configuracion.close()
            self.ventana_principal.resize(580, 420)

            self.mostrar_configuracion.setStatusTip('Mostrar menú de configuración')

        self.mostrando_menu_configuracion = not self.mostrando_menu_configuracion

    def accion_reiniciar_ventana(self) -> None: self.ventana_principal.reiniciar()

class BarraMenuPrincipal(QMenuBar):
    def __init__(self, parent = None) -> None:
        super().__init__(parent = parent)

        self.ventana_principal = self.parent()
        self.addMenu(MenuPrincipal('Menu', self))

        self.setStyleSheet(
            open(
                './gui/qss/menus.css', 'r'
            ).read()
        )