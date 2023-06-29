from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout
from superqt import QLabeledRangeSlider

from button import Button
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from settings_manager import SettingsManager
from list_enum import __TRUE__


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
        rename.stateChanged.connect(lambda val: self.settings.save_int_config('rename_file', val))

        tagger = QCheckBox(self.tr('Change Tag Files'))
        tagger.setFocusPolicy(Qt.NoFocus)
        tagger.stateChanged.connect(lambda val: self.settings.save_int_config('file_tagger', val))

        addnum = QCheckBox(self.tr('Maintain File Order'))
        addnum.setFocusPolicy(Qt.NoFocus)
        addnum.stateChanged.connect(lambda val: self.settings.save_int_config('file_addnum', val))

        rangeslider = QLabeledRangeSlider(Qt.Orientation.Horizontal)
        rangeslider.setFixedWidth(200)
        rangeslider.setRange(0, 60)
        rangeslider.setValue((self.settings.load_int_config('initial_range', defaultValue=10),
                              self.settings.load_int_config('final_range', defaultValue=20)))
        rangeslider.valueChanged.connect(self.save_range_position)

        if self.settings.load_int_config('rename_file') == __TRUE__:
            rename.setChecked(True)
        if self.settings.load_int_config('file_tagger') == __TRUE__:
            tagger.setChecked(True)
        if self.settings.load_int_config('file_addnum') == __TRUE__:
            addnum.setChecked(True)

        layoutck = QVBoxLayout()
        layoutck.addWidget(rename)
        layoutck.addWidget(tagger)
        layoutck.addWidget(addnum)
        layoutck.addWidget(rangeslider)

        layoutbtn = HBoxLayout(10)
        layoutbtn.addLayout(layoutck)
        layoutbtn.addSpacing(20)
        layoutbtn.addWidget(run)

        layout = GridLayout(rd='12', on_border=True)
        layout.addLayout(layoutbtn, 0, 0)

        self.setLayout(layout)

    # Ação ao iniciar a interface
    def showEvent(self, event):
        self.set_resize(self.point)

    # QPoint usado para o mover a janela
    def set_point(self, point) -> None:
        self.point = point

    # Função para mover a janela conforme a interface
    def set_resize(self, pos) -> None:
        self.move(pos.x() - 240, pos.y() + 42)
        self.show()

    # Emissão para avisar o programa que é para executar a busca ao fechar o diálogo
    def close_continue(self) -> None:
        self.run.emit()
        self.close()

    # Função para gravar os valores do qrangeslider
    def save_range_position(self, val) -> None:
        self.settings.save_int_config('initial_range', val[0])
        self.settings.save_int_config('final_range', val[1])
