from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle


# Delegate para impedir a seleção e o realce de colunas específicas
class ListDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # Definir a cor da seleção
        if option.state & QStyle.State_Selected:
            palette = option.palette
            highlight_color = palette.color(QPalette.Highlight)
            highlight_color.setAlpha(100)
            palette.setColor(QPalette.Highlight, highlight_color)
            option.palette = palette

    def paint(self, painter, option, index):
        option.state &= ~QStyle.State_MouseOver
        super().paint(painter, option, index)
