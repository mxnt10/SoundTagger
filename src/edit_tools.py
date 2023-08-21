from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget

from src.edit_tags import editTags
from src.vboxlayout import VBoxLayout


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
            '    border: 1px solid rgb(76, 78, 79);'
            '    border-top-right-radius: 10px;'
            '    border-bottom-left-radius: 10px;'
            '    border-bottom-right-radius: 10px;'
            '    margin-left: 1;'
            '}'
            'QTabBar::tab {'
            '    border: 1px solid rgb(76, 78, 79);'
            '    border-top-left-radius: 10px;'
            '    border-top-right-radius: 10px;'
            '    padding: 5 25;'
            '}'
            'QTabBar::tab:selected {'
            '    background-color: rgb(27, 30, 32);'
            '}')

        lay = VBoxLayout()
        lay.addWidget(tab)

        self.setLayout(lay)

    def setFile(self, file):
        self.tag.setFile(file)

    def isFileSupported(self):
        return self.tag.isFileSupported()
