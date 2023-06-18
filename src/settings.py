from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout

from gridlayout import GridLayout
from settings_manager import SettingsManager


# Classe para as configurações
class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()

        # Configuração das APIs
        audd_api_text = QLineEdit()
        audd_api_text.textChanged.connect(self.changeValues)

        if self.settings.load_audd_api_key() is not None:
            audd_api_text.setText(self.settings.load_audd_api_key())

        # Layout para a API do audD
        audd_api = QHBoxLayout()
        audd_api.addWidget(QLabel('audD API Token'))
        audd_api.addWidget(audd_api_text)

        # Layout para posicionar os widgets
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        layout.addSpacing(20)
        layout.addLayout(audd_api)
        layout.addStretch(1)

        # layout para inserir o fundo
        main_layout = GridLayout(None, 0)
        main_layout.addLayout(layout, 0, 0)

        self.setLayout(main_layout)

    # Alterar a configuração chave da API audD
    def changeValues(self, text):
        if self.settings.load_audd_api_key() == text:
            return
        self.settings.save_audd_api_key(text)
