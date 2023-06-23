from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout

from button import Button
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from settings_manager import SettingsManager


# Classe para configurar ajustes antes de iniciar a busca
class RunOptions(QWidget):
    run = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.settings = SettingsManager()
        self.point = None

        run = Button('run', self.tr('Run Process'))
        run.clicked.connect(self.close_continue)

        rename = QCheckBox(self.tr('Rename'))
        rename.setFocusPolicy(Qt.NoFocus)
        rename.stateChanged.connect(lambda val: self.settings.save_rename_file(val))

        tagger = QCheckBox(self.tr('Edit Tag Files'))
        tagger.setFocusPolicy(Qt.NoFocus)
        tagger.stateChanged.connect(lambda val: self.settings.save_file_tagger(val))

        if self.settings.load_rename_file() == '2':
            rename.setChecked(True)

        if self.settings.load_file_tagger() == '2':
            tagger.setChecked(True)

        layoutck = QVBoxLayout()
        layoutck.addWidget(rename)
        layoutck.addWidget(tagger)

        layoutbtn = HBoxLayout(10)
        layoutbtn.addLayout(layoutck)
        layoutbtn.addSpacing(20)
        layoutbtn.addWidget(run)

        layout = GridLayout(None, 5, '245')
        layout.addLayout(layoutbtn, 0, 0)

        self.setLayout(layout)

    # Ação ao iniciar a interface
    def showEvent(self, event):
        self.set_resize(self.point)

    # QPoint usado para o mover a janela
    def set_point(self, point):
        self.point = point

    # Função para mover a janela conforme a interface
    def set_resize(self, pos):
        self.move(pos.x() - 240, pos.y() + 42)
        self.show()

    # Emissão para avisar o programa que é para executar a busca ao fechar o diálogo
    def close_continue(self):
        self.run.emit()
        self.close()
