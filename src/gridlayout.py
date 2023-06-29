from PyQt5.QtWidgets import QGridLayout, QWidget


# O background foi inserido na interface de forma isolada, se for inserir a folha de estilo nos widgets
# diretamente, o estilo será aplicado a todos os widgets filhos. Não é isso que eu quero, então por isso o backgroud
# foi feito com widgets de forma isolada. Pra facilitar, foi feita uma classe pra isso.
class GridLayout(QGridLayout):
    def __init__(self, parent=None, n=5, bg='255', rd='20', on_border=False):
        self.bg = bg
        self.n = n
        self.rd = rd
        self.on_border = on_border
        super().__init__(parent)
        self.setContentsMargins(self.n, self.n, self.n, self.n)

        border = ' border: 1px solid #444;'
        if self.on_border is False:
            border = ''

        style = 'background-color: rgba(42, 46, 50, ' + self.bg + '); border-radius: ' + self.rd + 'px;' + border

        widget = QWidget()
        widget.setStyleSheet(style)

        self.addWidget(widget, 0, 0)
