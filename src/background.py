import os
import random

from PyQt5.QtCore import QObject


# Classe para gerar uma folha de estilo para servir como plano de fundo
class Background(QObject):
    def __init__(self):
        super().__init__()
        self.bg_dir = self.get_local_image()

    # Buscando pelas imagens
    @staticmethod
    def get_local_image():
        def_dir = "/usr/share/SoundTagger/backgrounds"
        rel_dir = os.path.abspath("../backgrounds")
        if os.path.exists(def_dir):
            return def_dir
        if os.path.exists(rel_dir):
            return rel_dir
        return os.path.abspath("backgrounds")

    # Gerando números aleatórios com base nas imagens disponíveis
    def random(self):
        return str(random.randint(0, len(os.listdir(self.bg_dir)) - 1))

    # Gerando a folha de estilo
    def get_background(self):
        return str(
            f'QMainWindow {{'
            f'    border-image: url("{self.bg_dir}/bg{self.random()}.jpg");'
            f'    background-position: center; '
            f'}}'
        )
