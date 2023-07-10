from PyQt5.QtWidgets import QGridLayout, QWidget


# O background foi inserido na interface de forma isolada, se for inserir a folha de estilo nos widgets
# diretamente, o estilo será aplicado a todos os widgets filhos. Não é isso que eu quero, então por isso o backgroud
# foi feito com widgets de forma isolada. Pra facilitar, foi feita uma classe pra isso.
class GridLayout(QGridLayout):
    def __init__(self, parent=None, layout=None, margin=5, bg='255', radius='22', spacing=0, on_border=False):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

        border = ' border: 1px solid #444;'
        if on_border is False:
            border = str()

        style = 'background-color: rgba(42, 46, 50, ' + bg + '); border-radius: ' + radius + 'px;' + border

        widget = QWidget()
        widget.setStyleSheet(style)

        self.addWidget(widget, 0, 0)

        if layout is not None:
            self.addLayout(layout, 0, 0)
