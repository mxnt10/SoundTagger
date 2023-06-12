from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
import os


# Classe para definir o ícone do programa
class IconPrg(QObject):
    def __init__(self):
        super().__init__()

    # Função estática que define o ícone
    @staticmethod
    def get_icon():
        def_icon = "/usr/share/pixmaps/SoundTagger.png"
        rel_icon = os.path.abspath("../common") + "/SoundTagger.png"
        alt_icon = os.path.abspath("common") + "/SoundTagger.png"
        if os.path.exists(def_icon):
            return QIcon(def_icon)
        if os.path.exists(rel_icon):
            return QIcon(rel_icon)
        if os.path.exists(alt_icon):
            return QIcon(alt_icon)
        return QIcon()
