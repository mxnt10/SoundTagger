from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QLabel, QTextEdit

from gridlayout import GridLayout


# Customização do layout para personalizar a interface mais facilmente
class Form(QHBoxLayout):
    changeText = pyqtSignal(str)

    def __init__(self, label, margin=5, orig=False, min_size=100, d=':', space=5, form='line'):
        self.n = margin
        super().__init__()
        self.setContentsMargins(self.n, self.n, self.n, self.n)
        self.setSpacing(space)

        self.form = QTextEdit() if form == 'text' else QLineEdit()
        self.form.setAutoFillBackground(True)
        self.form.textChanged.connect((lambda v: self.changeText.emit(v)) if type(self.form) == QLineEdit else
                                      (lambda: self.changeText.emit(self.form.toPlainText())))

        labels = QLabel(label + ':' if d == ':' else label)
        if orig is False:
            labels.setMinimumWidth(min_size)
            labels.setAlignment(Qt.AlignRight if type(self.form) == QLineEdit else (Qt.AlignTop | Qt.AlignRight))
        else:
            labels.setAlignment(Qt.AlignLeft)

        self.addWidget(labels)

        if type(self.form) == QLineEdit:
            self.form.setStyleSheet(
                'QLineEdit {'
                '    border-radius: 16px;'
                '    padding: 6px;'
                '    padding-left: 12px;'
                '}'
                'QLineEdit:disabled {'
                '    background-color: #5f6265;'
                '}'
            )

            self.addWidget(self.form)
        else:
            self.form.setStyleSheet(
                'QTextEdit {'
                '    padding: 5px;'
                '    padding-left: 10px;'
                '    background-color: transparent;'
                '    border: none; '
                '}'
            )

            grid = GridLayout(margin=0, layout=self.form)
            grid.customStyle(
                'QWidget {'
                '    background-color: rgb(27, 30, 32);'
                '    border-top-left-radius: 8px;'
                '    border-top-right-radius: 16px;'
                '    border-bottom-left-radius: 16px;'
                '    border-bottom-right-radius: 16px;'
                '}'
            )

            self.addLayout(grid)

    # Precisa para setar o texto nos formulários
    def setText(self, txt) -> None:
        self.form.setText(txt)

    # Algumas condições precisam acessar se o formulário está vazio
    def text(self):
        return self.form.text() if type(self.form) == QLineEdit else self.form.toPlainText()

    # Alterando a edição dos campos do formulário
    def setEnabled(self, bol) -> None:
        self.form.setEnabled(bol)
