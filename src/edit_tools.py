from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QTabWidget

from edit_tags import editTags
from theme import Theme
from vboxlayout import VBoxLayout

########################################################################################################################


class editTools(QWidget):
    def __init__(self):
        super().__init__()

        self.tag = editTags()

        tab = QTabWidget()
        tab.setFocusPolicy(Qt.NoFocus)
        tab.addTab(self.tag, 'IdTags')

        tab.setStyleSheet(
            f'QTabWidget::pane {{'
            f'    background-color: transparent;'
            f'    border: 1px solid {Theme.color_palette(QPalette.Light)};'
            f'    border-top-right-radius: 14px;'
            f'    border-bottom-left-radius: 14px;'
            f'    border-bottom-right-radius: 14px;'
            f'    margin-left: 1;'
            f'}}'
            f'QTabBar::tab {{'
            f'    border: 1px solid {Theme.color_palette(QPalette.Light)};'
            f'    border-top-left-radius: 10px;'
            f'    border-top-right-radius: 10px;'
            f'    padding: 5 25;'
            f'}}'
            f'QTabBar::tab:selected {{'
            f'    background-color: {Theme.color_palette(QPalette.Base)};'
            f'}}'
        )

        lay = VBoxLayout()
        lay.addWidget(tab)

        self.setLayout(lay)

########################################################################################################################

    # Setando arquivos de mídia no formulário para exibir as tags
    def setFile(self, file):
        self.tag.setFile(file)

    # Verificando suporte de arquivos de mídia recém importados
    def isFileSupported(self):
        return self.tag.isFileSupported()
