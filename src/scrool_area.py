from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QScrollArea

from theme import Theme


# Classe que serve mais para separar a estilização do QScrollArea do que outra coisa
class ScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        hand = Theme.color_palette(QPalette.Light)

        self.setStyleSheet(
            f'QScrollArea {{'
            f'    border: none; '
            f'}}'
            f'QScrollBar:vertical {{'
            f'    border: none;'
            f'    background-color: transparent;'
            f'    width: 10px;'
            f'}}'
            f'QScrollBar:horizontal {{'
            f'    border: none;'
            f'    background-color: transparent;'
            f'    height: 10px;'
            f'}}'
            f'QScrollBar::handle:vertical {{'
            f'    background-color: {hand};'
            f'    min-height: 10px;'
            f'    border-radius: 5px;'
            f'    border: 2px solid transparent;'
            f'}}'
            f'QScrollBar::handle:horizontal {{'
            f'    background-color: {hand};'
            f'    min-width: 10px;'
            f'    border-radius: 5px;'
            f'    border: 2px solid transparent;'
            f'}}'
            f'QScrollBar::add-line, QScrollBar::sub-line {{'
            f'    background: none;'
            f'}}'
            f'QScrollBar::add-page, QScrollBar::sub-page {{'
            f'    background: none;'
            f'}}'
        )
