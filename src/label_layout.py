from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtWidgets import QHBoxLayout, QLabel


# Customização para o label para o about
class LabelLayout(QHBoxLayout):
    def __init__(self, text1, text2=None, blue=False, italic=True, bold=True, pointsize=(-1), one=False):
        self.pointsize = pointsize
        self.one = one

        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(QMargins())

        self.font = QFont()
        if self.pointsize > (-1):
            self.font.setPointSize(self.pointsize)
        self.font.setBold(bold)

        self.label1 = QLabel(text1)
        self.label1.setFont(self.font)

        self.addWidget(self.label1)

        if self.one is False:
            self.label1.setText(self.label1.text() + ': ')

            self.font.setBold(False)
            self.font.setItalic(italic)

            self.label2 = QLabel(text2)
            self.label2.setFont(self.font)

            if blue:
                pal = QPalette()
                pal.setColor(QPalette.WindowText, pal.color(QPalette.Highlight))
                self.label2.setPalette(pal)

            self.addWidget(self.label2)

    # Mudar o tamanho da fonte do label
    def set_point_size(self, size) -> None:
        self.font.setPointSize(size)
        self.label1.setFont(self.font)
        if self.one is False:
            self.label2.setFont(self.font)
