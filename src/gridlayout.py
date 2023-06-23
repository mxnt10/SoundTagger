from PyQt5.QtWidgets import QGridLayout, QWidget


# O background foi inserido na interface de forma isolada, se for inserir a folha de estilo nos widgets
# diretamente, o estilo será aplicado a todos os widgets filhos. Não é isso que eu quero, então por isso o backgroud
# foi feito com widgets de forma isolada. Pra facilitar, foi feita uma classe pra isso.
class GridLayout(QGridLayout):
    def __init__(self, parent=None, n=5, bg='220'):
        self.bg = bg
        self.n = n
        super().__init__(parent)
        self.setContentsMargins(self.n, self.n, self.n, self.n)

        style = 'background-color: rgba(42, 46, 50, ' + self.bg + '); border-radius: 20px;'

        widget = QWidget()
        widget.setStyleSheet(style)

        self.addWidget(widget, 0, 0)
