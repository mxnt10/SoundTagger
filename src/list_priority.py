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
            'QListWidget {'
            '    background-color: ' + t.color_palette(QPalette.Base) + ';'
            '    border: 1px solid ' + t.color_line() + ';'
            '    border-top-left-radius: 6px;'
            '    border-top-right-radius: 12px;'
            '    border-bottom-left-radius: 12px;'
            '    border-bottom-right-radius: 12px;'
            '}'
            'QListWidget:hover {'
            '    border: 1px solid ' + t.color_rgba(QPalette.Highlight, t.__LINE__) + ';'
            '}'
            'QListWidget::Item:unselected {'
            '    border: 1px solid transparent;'
            '    border-radius: 12px;'
            '    padding: 0 5;'
            '}'
            'QListWidget::Item:hover {'
            '    border: 1px solid transparent;'
            '    background-color: ' + t.color_rgba(QPalette.Highlight, t.__UNSELECT__) + ';'
            '    border-radius: 12px;'
            '    padding: 0 5;'
            '}'
            'QListWidget::Item:selected {'
            '    border: 1px solid transparent;'
            '    background-color: ' + t.color_rgba(QPalette.Highlight, t.__SELECT__) + ';'
            '    border-radius: 12px;'
            '    padding: 0 5;'
            '}'
        )

        self.model().rowsMoved.connect(lambda: self.clearSelection())

    # É só pra alterar a ordem não precisa manter selecionado
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.clearSelection()
        super().mouseReleaseEvent(event)
