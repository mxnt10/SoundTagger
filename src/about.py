from PyQt5.QtWidgets import QWidget, QLabel
from gridlayout import GridLayout


# Classe para as informações do programa
class About(QWidget):
    def __init__(self):
        super().__init__()

        layout = GridLayout(None, 0)
        layout.addWidget(QLabel(' SoundTagger v1.0 alpha'), 0, 0)

        self.setLayout(layout)
