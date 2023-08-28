from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPalette, QBrush, QPainter
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem

from theme import Theme


# Delegate para realçar e selecionar as colunas
class ListDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        self.this = parent
        super().__init__(parent)
        self.t = Theme()

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        if option.state & QStyle.State_Selected:
            palette = option.palette
            palette.setColor(QPalette.Highlight, Qt.transparent)
            option.palette = palette

    def paint(self, painter, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        # Verifique se o mouse está sobre a linha
        if options.state & QStyle.State_MouseOver:
            options.state &= ~QStyle.State_MouseOver

            # Realce padrão da seleção com semitransparência
            highlight_color = QPalette().color(QPalette.Highlight)
            highlight_color.setAlpha(self.t.__UNSELECT__)

            # Realce de toda a linha selecionada
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(highlight_color))
            painter.drawRoundedRect(QRect(0, option.rect.top(), self.this.width() - 10, option.rect.height()), 16, 16)
            painter.restore()

        super().paint(painter, options, index)
