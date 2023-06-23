from PyQt5.QtWidgets import QStyledItemDelegate, QStyle


# Delegate para impedir a seleção e o realce de colunas específicas
class ListDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.state &= ~QStyle.State_MouseOver
        if index.column() != 1:
            option.state &= ~QStyle.State_Selected
        super().paint(painter, option, index)