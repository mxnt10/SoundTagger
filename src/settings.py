from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem

from gridlayout import GridLayout
from settings_manager import SettingsManager
from hboxlayout import HBoxLayout


# Classe para as configurações
class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()

        # Lista de prioridade de uso das APIs
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setFixedSize(300, 100)

        for i in self.settings.load_priorities_API().split(':'):
            self.list_widget.addItem(QListWidgetItem(i))

        self.list_widget.model().rowsMoved.connect(self.onCurrentRowChanged)

        # Configuração das APIs
        audd_api_text = QLineEdit()
        audd_api_text.setText(str(self.settings.load_api_key('audD_API')))
        audd_api_text.textChanged.connect(lambda val: self.changeValues('audD_API', val))
        acoustid_api_text = QLineEdit()
        acoustid_api_text.setText(str(self.settings.load_api_key('acoustID_API')))
        acoustid_api_text.textChanged.connect(lambda val: self.changeValues('acoustID_API', val))

        # Labels
        audd_text = QLabel(self.tr('audD API Token'))
        audd_text.setAlignment(Qt.AlignRight)
        audd_text.setMinimumWidth(120)
        acoustid_text = QLabel(self.tr('AcoustID API Key'))
        acoustid_text.setAlignment(Qt.AlignRight)
        acoustid_text.setMinimumWidth(120)
        priority_text = QLabel(self.tr('Priority'))
        priority_text.setAlignment(Qt.AlignRight | Qt.AlignTop)
        priority_text.setMinimumWidth(120)

        # Layout da lista de prioridade
        list_layout = HBoxLayout(array_widgets=[priority_text, self.list_widget])
        list_layout.addStretch(1)

        # Layout para a API do audD
        audd_api = HBoxLayout(array_widgets=[audd_text, audd_api_text])

        # Layout para a API do AcoustID
        acoustid_api = HBoxLayout(array_widgets=[acoustid_text, acoustid_api_text])

        # Layout para posicionar os widgets
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        layout.addSpacing(20)
        layout.addLayout(list_layout)
        layout.addSpacing(20)
        layout.addLayout(audd_api)
        layout.addSpacing(20)
        layout.addLayout(acoustid_api)
        layout.addSpacing(20)
        layout.addStretch(1)

        self.setLayout(GridLayout(margin=0, spacing=10, layout=layout))

    # Alterar a configuração chave da API audD
    def changeValues(self, key, text):
        if self.settings.load_api_key(key) == text:
            return
        self.settings.save_api_key(key, text)

    # Salvando a lista de prioridade das APIs
    def onCurrentRowChanged(self):
        order = ":".join([self.list_widget.item(i).text() for i in range(self.list_widget.count())])
        self.settings.save_priorities_API(order)
