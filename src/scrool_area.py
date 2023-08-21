from PyQt5.QtWidgets import QScrollArea


# Classe que serve mais para separar a estilização do QScrollArea do que outra coisa
class ScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)

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
            '    background-color: #75797e;'
            '    min-height: 10px;'
            '    border-radius: 5px;'
            '    border: 2px solid transparent;'
            '}'
            'QScrollBar::handle:horizontal {'
            '    background-color: #75797e;'
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
