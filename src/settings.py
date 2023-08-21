from PyQt5.QtCore import Qt, QMargins, QSize
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QLabel

from button import Button
from form import Form
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from list_priority import ListPriority
from settings_manager import SettingsManager
from vboxlayout import VBoxLayout


########################################################################################################################


# Classe para as configurações
class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()

        # Lista de prioridade de uso das APIs
        self.list_widget = ListPriority(QSize(300, 100))

        for i in self.settings.load_priorities_API().split(':'):
            self.list_widget.addItem(QListWidgetItem(i))

        self.list_widget.model().rowsMoved.connect(self.onCurrentRowChanged)

        # Configuração das APIs
        self.audd_api = Form(self.tr('audD API Token'), min_size=110, d=str())
        self.audd_api.setText(str(self.settings.load_api_key('audD_API')))
        self.audd_api.changeText.connect(lambda val: self.changeValues('audD_API', val))
        self.acoustid_api = Form(self.tr('AcoustID API Key'), min_size=110, d=str())
        self.acoustid_api.setText(str(self.settings.load_api_key('acoustID_API')))
        self.acoustid_api.changeText.connect(lambda val: self.changeValues('acoustID_API', val))

        # Label
        priority_text = QLabel(self.tr('Priority'))
        priority_text.setMinimumWidth(120)
        priority_text.setAlignment((Qt.AlignRight | Qt.AlignTop))

        # Botões
        audd_clean = Button("remove-list", size=38)
        audd_clean.clicked.connect(lambda: self.cleanValues('audD_API'))
        acoustid_clean = Button("remove-list", size=38)
        acoustid_clean.clicked.connect(lambda: self.cleanValues('acoustID_API'))

        # Layout para a lista de prioridade e APIs
        list_layout = HBoxLayout(array_widgets=[priority_text, self.list_widget, 'S'])
        audd_api = HBoxLayout(array_widgets=[self.audd_api, audd_clean], space=0)
        acoustid_api = HBoxLayout(array_widgets=[self.acoustid_api, acoustid_clean], space=0)

        # Layout para posicionar os widgets
        layout = VBoxLayout(margin=QMargins(15, 5, 15, 5),
                            array_widgets=[20, list_layout, 20, audd_api, 20, acoustid_api, 20, 'S'])

        self.setLayout(GridLayout(margin=0, space=10, layout=layout))

########################################################################################################################

    # Alterar as configurações das chaves de APIS
    def changeValues(self, key, text):
        if self.settings.load_api_key(key) == text:
            return
        self.settings.save_api_key(key, text)

    # Limpando as configurações das chaves de APIS
    def cleanValues(self, key):
        if key == 'audD_API':
            self.audd_api.setText(str())
            return
        if key == 'acoustID_API':
            self.acoustid_api.setText(str())

    # Salvando a lista de prioridade das APIs
    def onCurrentRowChanged(self) -> None:
        order = ":".join([self.list_widget.item(i).text() for i in range(self.list_widget.count())])
        self.settings.save_priorities_API(order)
