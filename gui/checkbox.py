#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from qtpy.QtWidgets import QCheckBox

class CheckBox(QCheckBox):
    def __init__(self, texto: str, parent = None) -> None:
        super().__init__(texto, parent = parent)

        self.setStyleSheet(
            open('./gui/qss/checkbox.css', 'r').read()
        )