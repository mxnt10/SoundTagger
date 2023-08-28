from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget
from superqt import QLabeledRangeSlider

from button import Button
from checkbox import CheckBox
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from settings_manager import SettingsManager
from vboxlayout import VBoxLayout


########################################################################################################################


# Classe para configurar ajustes antes de iniciar a busca
class RunOptions(QWidget):
    run = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.settings = SettingsManager()
        self.point = None
        self.size = QSize()
        self.x = 100

        run = Button('apply', self.tr('Run Process'))
        run.clicked.connect(self.close_continue)

        rename = CheckBox(self.tr('Rename Files'), self.settings.load_int_convert_bool('rename_file'))
        rename.stateChanged.connect(lambda val: self.settings.save_int_config('rename_file', val))

        tagger = CheckBox(self.tr('Change Tag Files'), self.settings.load_int_convert_bool('file_tagger'))
        tagger.stateChanged.connect(lambda val: self.settings.save_int_config('file_tagger', val))

        addnum = CheckBox(self.tr('Maintain File Order'), self.settings.load_int_convert_bool('file_addnum'))
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

        layoutbtn = HBoxLayout(margin=10, array_widgets=[layoutck, 20, run])
        layoutbtn.setAlignment(run, Qt.AlignBottom)

        self.setLayout(GridLayout(layout=layoutbtn, radius='16', on_border=True))

########################################################################################################################

    # QPoint usado para o mover a janela
    def set_point(self, point) -> None:
        if self.settings.priority_api() == 'acoustID':
            self.rangeslider.setVisible(False)
            self.size = QSize(320, 120)
            self.x = 120
        else:
            self.rangeslider.setVisible(True)
            self.size = QSize(400, 170)
            self.x = 160

        self.point = point

    # Função para mover a janela conforme a interface
    def set_resize(self, pos) -> None:
        self.setFixedSize(self.size)
        self.move(pos.x() - self.x, pos.y() + 50)
        self.show()

    # Emissão para avisar o programa que é para executar a busca ao fechar o diálogo
    def close_continue(self) -> None:
        self.run.emit()
        self.close()

    # Função para gravar os valores do qrangeslider
    def save_range_position(self, val) -> None:
        self.settings.save_int_config('initial_range', val[0])
        self.settings.save_int_config('final_range', val[1])

########################################################################################################################

    # Ação ao iniciar a interface
    def showEvent(self, event):
        self.set_resize(self.point)

    # Trancando o clique do mouse nesse widget
    def mouseReleaseEvent(self, event):
        pass
