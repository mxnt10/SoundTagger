from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QTabWidget

from edit_tags import editTags
from theme import Theme
from vboxlayout import VBoxLayout


class editTools(QWidget):
    def __init__(self):
        super().__init__()

        self.tag = editTags()

        tab = QTabWidget()
        tab.setFocusPolicy(Qt.NoFocus)
        tab.addTab(self.tag, 'IdTags')

        tab.setStyleSheet(
            'QTabWidget::pane {'
            '    background-color: transparent;'
            '    border: 1px solid ' + Theme.color_palette(QPalette.Light) + ';'
            '    border-top-right-radius: 14px;'
            '    border-bottom-left-radius: 14px;'
            '    border-bottom-right-radius: 14px;'
            '    margin-left: 1;'
            '}'
            'QTabBar::tab {'
            '    border: 1px solid ' + Theme.color_palette(QPalette.Light) + ';'
            '    border-top-left-radius: 10px;'
            '    border-top-right-radius: 10px;'
            '    padding: 5 25;'
            '}'
            'QTabBar::tab:selected {'
            '    background-color: ' + Theme.color_palette(QPalette.Base) + ';'
            '}')

        lay = VBoxLayout()
        lay.addWidget(tab)

        self.setLayout(lay)

    def setFile(self, file):
        self.tag.setFile(file)

    def isFileSupported(self):
        return self.tag.isFileSupported()
