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

        # Widgets dos botões
        self.btn = QWidget()

        # Widgets para editar as tags
        self.tag = editTags()
        self.tag.visible.connect(lambda: self.btn.setVisible(True))

        self.tab = QTabWidget()
        self.tab.setFocusPolicy(Qt.NoFocus)
        self.tab.addTab(self.tag, 'IdTags')

        apply = Button(text='apply', size=42, ajust=8, select=3, click=2)
        apply.clicked.connect(self.set_apply)
        cancel = Button(text='clean', size=42, ajust=8, select=3, click=2)
        cancel.clicked.connect(self.set_cancel)

        buttons = HBoxLayout(parent=self.btn, array_widgets=[apply, cancel, 'S'], margin=3)

        for i in range(buttons.count()):
            buttons.itemAt(i).setAlignment(Qt.AlignLeft)

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

        lay = VBoxLayout(array_widgets=[self.tab, self.btn], margin=0)
        self.setLayout(lay)

########################################################################################################################

    # Setando arquivos de mídia no formulário para exibir as tags
    def set_file(self, file) -> None:
        self.tag.set_file(file)
        self.selected_change = file

    # Verificando suporte de arquivos de mídia recém importados
    def is_file_supported(self):
        return self.tag.is_file_supported()

    # Aplicando alterações de tags
    def set_apply(self) -> None:
        if self.tab.currentIndex() == 0:
            self.tag.apply_tags(self.selected_change)
            self.btn.setVisible(False)

    # Descartar alterações de tags
    def set_cancel(self) -> None:
        if self.tab.currentIndex() == 0:
            if self.selected_change is not None:
                self.tag.set_file(self.selected_change)
                self.btn.setVisible(False)
