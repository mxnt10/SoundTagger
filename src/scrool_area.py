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
            'QScrollArea {'
            '    border: none; '
            '}'
            'QScrollBar:vertical {'
            '    border: none;'
            '    background-color: transparent;'
            '    width: 10px;'
            '}'
            'QScrollBar:horizontal {'
            '    border: none;'
            '    background-color: transparent;'
            '    height: 10px;'
            '}'
            'QScrollBar::handle:vertical {'
            '    background-color: ' + hand + ';'
            '    min-height: 10px;'
            '    border-radius: 5px;'
            '    border: 2px solid transparent;'
            '}'
            'QScrollBar::handle:horizontal {'
            '    background-color: ' + hand + ';'
            '    min-width: 10px;'
            '    border-radius: 5px;'
            '    border: 2px solid transparent;'
            '}'
            'QScrollBar::add-line, QScrollBar::sub-line {'
            '    background: none;'
            '}'
            'QScrollBar::add-page, QScrollBar::sub-page {'
            '    background: none;'
            '}'
        )
