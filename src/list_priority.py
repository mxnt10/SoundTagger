from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QListWidget


# Classe para a lista de prioridade
class ListPriority(QListWidget):
    def __init__(self, size):
        super().__init__()
        self.setFixedSize(size)
        self.setFocusPolicy(Qt.NoFocus)
        self.setDragDropMode(QListWidget.InternalMove)

        self.setStyleSheet(
            'QListWidget {'
            '    background-color: rgb(27, 30, 32);'
            '    border: 6px solid rgb(27, 30, 32);'
            '    border-top-left-radius: 8px;'
            '    border-top-right-radius: 18px;'
            '    border-bottom-left-radius: 18px;'
            '    border-bottom-right-radius: 18px;'
            '}'
            'QListWidget::Item:unselected {'
            '    border-radius: 12px;'
            '    padding: 0 5;'
            '}'
            'QListWidget::Item:hover {'
            '    background-color: rgba(61, 174, 233, 20);'
            '    border-radius: 12px;'
            '    padding: 0 5;'
            '}'
            'QListWidget::Item:selected {'
            '    background-color: rgba(61, 174, 233, 80);'
            '    border-radius: 12px;'
            '    padding: 0 5;'
            '}'
        )

        self.model().rowsMoved.connect(lambda: self.clearSelection())

    # É só pra alterar a ordem não precisa manter selecionado
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.clearSelection()
        super().mouseReleaseEvent(event)
