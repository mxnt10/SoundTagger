from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QLabel, QTextEdit

from gridlayout import GridLayout
from theme import Theme

########################################################################################################################


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

        labels = QLabel(f'{label}:' if d == ':' else label)
        if orig is False:
            labels.setMinimumWidth(min_size)
            labels.setAlignment(Qt.AlignRight if type(self.form) == QLineEdit else (Qt.AlignTop | Qt.AlignRight))
        else:
            labels.setAlignment(Qt.AlignLeft)

        self.addWidget(labels)
        self.t = Theme()

        if type(self.form) == QLineEdit:
            self.form.setStyleSheet(
                f'QLineEdit {{'
                f'    border: 1px solid {self.t.color_line()};'
                f'    border-radius: 16px;'
                f'    padding: 6px;'
                f'    padding-left: 12px;'
                f'}}'
                f'QLineEdit:disabled {{'
                f'    border: 1px solid {self.t.color_line()};'
                f'    background-color: {self.t.color_palette(QPalette.Midlight)};'
                f'}}'
                f'QLineEdit:hover {{'
                f'    border: 1px solid {self.t.color_rgba(QPalette.Highlight, self.t.__LINE__)};'
                f'}}'
            )

            self.addWidget(self.form)
        else:
            self.form.setStyleSheet(
                'QTextEdit {'
                '    margin: 8px;'
                '    padding: -4 2;'
                '    background-color: transparent;'
                '    border: none; '
                '}'
            )

            self.grid = GridLayout(margin=0, layout=self.form)
            self.grid.customStyle(
                f'QWidget {{'
                f'    border: 1px solid {self.t.color_line()};'
                f'    background-color: {self.t.color_palette(QPalette.Base)};'
                f'    border-top-left-radius: 6px;'
                f'    border-top-right-radius: 18px;'
                f'    border-bottom-left-radius: 18px;'
                f'    border-bottom-right-radius: 18px;'
                f'}}'
            )

            self.form.enterEvent = self.focusStyle
            self.form.leaveEvent = self.customStyle

            self.addLayout(self.grid)

########################################################################################################################

    # Precisa para setar o texto nos formulários
    def setText(self, txt) -> None:
        self.form.setText(txt)

    # Algumas condições precisam acessar se o formulário está vazio
    def text(self):
        return self.form.text() if type(self.form) == QLineEdit else self.form.toPlainText()

    # Alterando a edição dos campos do formulário
    def setEnabled(self, bol) -> None:
        self.form.setEnabled(bol)

    def focusStyle(self, event) -> None:
        _ = event
        self.grid.customStyle(
            f'QWidget {{'
            f'    border: 1px solid {self.t.color_rgba(QPalette.Highlight, self.t.__LINE__)};'
            f'    background-color: {self.t.color_palette(QPalette.Base)};'
            f'    border-top-left-radius: 6px;'
            f'    border-top-right-radius: 18px;'
            f'    border-bottom-left-radius: 18px;'
            f'    border-bottom-right-radius: 18px;'
            f'}}'
        )

    def customStyle(self, event) -> None:
        _ = event
        self.grid.customStyle(
            f'QWidget {{'
            f'    border: 1px solid {self.t.color_line()};'
            f'    background-color: {self.t.color_palette(QPalette.Base)};'
            f'    border-top-left-radius: 6px;'
            f'    border-top-right-radius: 18px;'
            f'    border-bottom-left-radius: 18px;'
            f'    border-bottom-right-radius: 18px;'
            f'}}'
        )
