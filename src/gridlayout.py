from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from theme import Theme


# O background foi inserido na interface de forma isolada, se for inserir a folha de estilo nos widgets
# diretamente, o estilo será aplicado a todos os widgets filhos. Não é isso que eu quero, então por isso o backgroud
# foi feito com widgets de forma isolada. Pra facilitar, foi feita uma classe pra isso.
class GridLayout(QGridLayout):
    def __init__(self, parent=None, layout=None, margin=5, radius='22', space=0, on_border=False):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(space)
        t = Theme()

        border = f' border: 1px solid {t.color_palette(QPalette.Light)};'
        if on_border is False:
            border = ''

        style = f'background-color: {t.color_palette(QPalette.Window)}; border-radius: {radius}px;{border}'

        self.widget = QWidget()
        self.widget.setStyleSheet(style)

        self.addWidget(self.widget, 0, 0)

        if layout is not None:
            if isinstance(layout, QHBoxLayout) or isinstance(layout, QVBoxLayout):
                self.addLayout(layout, 0, 0)
            else:
                self.addWidget(layout, 0, 0)

    # O widget do qtextedit é que vai ser customizado
    def custom_style(self, style) -> None:
        self.widget.setStyleSheet(style)
