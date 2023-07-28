from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox
from superqt import QLabeledRangeSlider

from button import Button
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from settings_manager import SettingsManager
from vboxlayout import VBoxLayout


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
        self.w = 280

        run = Button('apply', self.tr('Run Process'))
        run.clicked.connect(self.close_continue)

        rename = QCheckBox(self.tr('Rename'))
        rename.setFocusPolicy(Qt.NoFocus)
        rename.setChecked(self.settings.load_int_convert_bool('rename_file'))
        rename.stateChanged.connect(lambda val: self.settings.save_int_config('rename_file', val))

        tagger = QCheckBox(self.tr('Change Tag Files'))
        tagger.setFocusPolicy(Qt.NoFocus)
        tagger.setChecked(self.settings.load_int_convert_bool('file_tagger'))
        tagger.stateChanged.connect(lambda val: self.settings.save_int_config('file_tagger', val))

        addnum = QCheckBox(self.tr('Maintain File Order'))
        addnum.setFocusPolicy(Qt.NoFocus)
        addnum.setChecked(self.settings.load_int_convert_bool('file_addnum'))
        addnum.stateChanged.connect(lambda val: self.settings.save_int_config('file_addnum', val))

        layoutck = VBoxLayout(array_widgets=[rename, tagger, addnum])

        # Slider para selecionar parte da mídia para a busca
        self.rangeslider: QWidget = QLabeledRangeSlider(Qt.Horizontal)
        self.rangeslider.setFixedWidth(200)
        self.rangeslider.setRange(0, 60)
        self.rangeslider.setValue((self.settings.load_int_config('initial_range', defaultValue=10),
                                   self.settings.load_int_config('final_range', defaultValue=20)))
        self.rangeslider.valueChanged.connect(self.save_range_position)
        layoutck.addWidget(self.rangeslider)

        layoutbtn = HBoxLayout(margin=10)
        layoutbtn.addLayout(layoutck)
        layoutbtn.addSpacing(20)
        layoutbtn.addWidget(run)

        self.setLayout(GridLayout(layout=layoutbtn, radius='12', on_border=True))

    # Ação ao iniciar a interface
    def showEvent(self, event):
        self.set_resize(self.point)

    # QPoint usado para o mover a janela
    def set_point(self, point) -> None:
        if self.settings.priority_api() == 'acoustID':
            self.rangeslider.setVisible(False)
            self.w = 240
        else:
            self.rangeslider.setVisible(True)
            self.w = 280

        self.point = point

    # Função para mover a janela conforme a interface
    def set_resize(self, pos) -> None:
        self.move(pos.x() - self.w, pos.y() + 43)
        self.show()

    # Emissão para avisar o programa que é para executar a busca ao fechar o diálogo
    def close_continue(self) -> None:
        self.run.emit()
        self.close()

    # Função para gravar os valores do qrangeslider
    def save_range_position(self, val) -> None:
        self.settings.save_int_config('initial_range', val[0])
        self.settings.save_int_config('final_range', val[1])
