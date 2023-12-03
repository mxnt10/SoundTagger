from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtWidgets import QWidget

from button import Button
from gridlayout import GridLayout
from hboxlayout import HBoxLayout


# Botões da interface do programa
class Controls(HBoxLayout):
    control_add = pyqtSignal()
    control_remove = pyqtSignal()
    control_clean = pyqtSignal()
    control_options = pyqtSignal()
    control_point = pyqtSignal(QPoint)
    control_main = pyqtSignal()
    control_settings = pyqtSignal()
    control_about = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.bool = False

        # Botões da interface
        add = Button('add', tooltip=self.tr('Add Files'))
        add.clicked.connect(lambda: self.control_add.emit())
        self.remove = Button('remove', tooltip=self.tr('Remove File'))
        self.remove.clicked.connect(lambda: self.control_remove.emit())
        self.clean = Button('clean', tooltip=self.tr('Remove Selected Files'))
        self.clean.clicked.connect(lambda: self.control_clean.emit())
        self.run = Button('fingerprint', tooltip=self.tr('Search Music Information'))
        self.run.height.connect(lambda point: self.control_point.emit(point))
        self.run.clicked.connect(lambda: self.control_options.emit())
        main = Button('return', tooltip=self.tr('Return to Main'))
        main.clicked.connect(self.set_main)
        settings = Button('settings', tooltip=self.tr('Settings'))
        settings.clicked.connect(self.set_settings)
        about = Button('about', tooltip=self.tr('About'))
        about.clicked.connect(self.set_about)

        # Controle do botão main
        self.v_main = QWidget()
        self.v_main.setVisible(False)
        v_main_layout = GridLayout(parent=self.v_main)
        v_main_layout.addLayout(HBoxLayout(array_widgets=[main]), 0, 0)

        # Ajuste dos botões do menu principal
        self.v_buttons = QWidget()
        list_btn_layout = GridLayout(parent=self.v_buttons)
        list_btn_layout.addLayout(HBoxLayout(array_widgets=[add, self.remove, self.clean, 10, self.run]), 0, 0)

        # Ajuste dos botões e layout
        f_buttons = QWidget()
        f_buttons_layout = GridLayout(parent=f_buttons)
        f_buttons_layout.addLayout(HBoxLayout(array_widgets=[settings, about]), 0, 0)

        # Ajustes e botões para o layout
        self.setContentsMargins(0, 0, 0, 0)
        self.addWidget(self.v_buttons)
        self.addStretch(1)
        self.addWidget(self.v_main)
        self.addWidget(f_buttons)
        self.deactive_buttons()

    # Botão para retornar a lista de arquivos de mídia
    def set_main(self) -> None:
        self.v_buttons.setVisible(True)
        self.v_main.setVisible(False)
        self.control_main.emit()

    # Botão de configurações
    def set_settings(self) -> None:
        self.v_buttons.setVisible(False)
        self.v_main.setVisible(True)
        self.control_settings.emit()

    # Botão de sobre
    def set_about(self) -> None:
        self.v_buttons.setVisible(False)
        self.v_main.setVisible(True)
        self.control_about.emit()

    # Posição do botão run
    def posrun(self):
        return self.run.mapToGlobal(self.run.pos())

    # Ativar botões ao importar algum arquivo de mídia
    def deactive_buttons(self) -> None:
        self.remove.setVisible(False)
        self.clean.setVisible(False)
        self.run.setVisible(False)
        self.bool = False

    # Ativar botões ao importar algum arquivo de mídia
    def active_buttons(self) -> None:
        self.remove.setVisible(True)
        self.clean.setVisible(True)
        self.run.setVisible(True)
        self.bool = True
