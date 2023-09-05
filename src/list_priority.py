from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPalette
from PyQt5.QtWidgets import QListWidget

from theme import Theme


# Classe para a lista de prioridade
class ListPriority(QListWidget):
    def __init__(self, size):
        super().__init__()
        self.setFixedSize(size)
        self.setFocusPolicy(Qt.NoFocus)
        self.setDragDropMode(QListWidget.InternalMove)
        t = Theme()

        self.setStyleSheet(
            f'QListWidget {{'
            f'    background-color: {t.color_palette(QPalette.Base)};'
            f'    border: 1px solid {t.color_line()};'
            f'    border-top-left-radius: 6px;'
            f'    border-top-right-radius: 12px;'
            f'    border-bottom-left-radius: 12px;'
            f'    border-bottom-right-radius: 12px;'
            f'}}'
            f'QListWidget:hover {{'
            f'    border: 1px solid {t.color_rgba(QPalette.Highlight, t.__LINE__)};'
            f'}}'
            f'QListWidget::Item:unselected {{'
            f'    border: 1px solid transparent;'
            f'    border-radius: 12px;'
            f'    padding: 0 5;'
            f'}}'
            f'QListWidget::Item:hover {{'
            f'    border: 1px solid transparent;'
            f'    background-color: {t.color_rgba(QPalette.Highlight, t.__UNSELECT__)};'
            f'    border-radius: 12px;'
            f'    padding: 0 5;'
            f'}}'
            f'QListWidget::Item:selected {{'
            f'    border: 1px solid transparent;'
            f'    background-color: {t.color_rgba(QPalette.Highlight, t.__SELECT__)};'
            f'    border-radius: 12px;'
            f'    padding: 0 5;'
            f'}}'
        )

        self.model().rowsMoved.connect(lambda: self.clearSelection())

    # É só pra alterar a ordem não precisa manter selecionado
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.clearSelection()
        super().mouseReleaseEvent(event)
