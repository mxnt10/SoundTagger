from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QGridLayout, QHBoxLayout

from gridlayout import GridLayout


# Classe para as configurações
class Settings(QWidget):
    def __init__(self):
        super().__init__()

        # Configuração das APIs
        self.acoustid_api = QLineEdit()
        self.lastfm_api = QLineEdit()
        self.lastfm_secret = QLineEdit()

        # Layout para a API AcoustID
        acoustid = QHBoxLayout()
        acoustid.addWidget(QLabel('AcoustID API KEY'))
        acoustid.addWidget(self.acoustid_api)

        # Layout para a API last.fm
        lastfm = QGridLayout()
        lastfm.addWidget(QLabel('LastFM API KEY'), 0, 0)
        lastfm.addWidget(self.lastfm_api, 0, 1)
        lastfm.addWidget(QLabel('LastFM SECRET KEY'), 1, 0)
        lastfm.addWidget(self.lastfm_secret, 1, 1)

        # Layout para posicionar os widgets
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        layout.addSpacing(20)
        layout.addLayout(acoustid)
        layout.addSpacing(20)
        layout.addLayout(lastfm)
        layout.addStretch(1)

        # layout para inserir o fundo
        main_layout = GridLayout(None, 0)
        main_layout.addLayout(layout, 0, 0)

        self.setLayout(main_layout)
