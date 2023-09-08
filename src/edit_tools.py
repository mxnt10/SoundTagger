from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QTabWidget

from button import Button
from edit_tags import editTags
from hboxlayout import HBoxLayout
from theme import Theme
from vboxlayout import VBoxLayout


########################################################################################################################


class editTools(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_change = None

        self.tag = editTags()

        self.tab = QTabWidget()
        self.tab.setFocusPolicy(Qt.NoFocus)
        self.tab.addTab(self.tag, 'IdTags')

        apply = Button('apply')
        apply.clicked.connect(self.setApply)
        cancel = Button('clean')
        cancel.clicked.connect(self.setCancel)

        buttons = HBoxLayout(array_widgets=[apply, cancel, 'S'], margin=0)

        for i in range(buttons.count()):
            w = buttons.itemAt(i)
            w.setAlignment(Qt.AlignLeft)

        # Aplicando uma folha de estilo
        t = Theme()
        self.tab.setStyleSheet(
            f'QTabWidget::pane {{'
            f'    background-color: transparent;'
            f'    border: 1px solid {t.color_palette(QPalette.Light)};'
            f'    border-top-right-radius: 14px;'
            f'    border-bottom-left-radius: 14px;'
            f'    border-bottom-right-radius: 14px;'
            f'    margin-left: 1;'
            f'}}'
            f'QTabBar::tab {{'
            f'    border: 1px solid {t.color_palette(QPalette.Light)};'
            f'    border-top-left-radius: 10px;'
            f'    border-top-right-radius: 10px;'
            f'    padding: 5 25;'
            f'}}'
            f'QTabBar::tab:selected {{'
            f'    background-color: {t.color_palette(QPalette.Base)};'
            f'}}'
        )

        lay = VBoxLayout(array_widgets=[self.tab, buttons], margin=0)
        self.setLayout(lay)

########################################################################################################################

    # Setando arquivos de mídia no formulário para exibir as tags
    def setFile(self, file):
        self.tag.setFile(file)
        self.selected_change = file

    # Verificando suporte de arquivos de mídia recém importados
    def isFileSupported(self):
        return self.tag.isFileSupported()

    # Aplicando alterações de tags
    def setApply(self):
        if self.tab.currentIndex() == 0:
            self.tag.applyTags(self.selected_change)

    # Descartar alterações de tags
    def setCancel(self):
        if self.tab.currentIndex() == 0:
            if self.selected_change is not None:
                self.tag.setFile(self.selected_change)
